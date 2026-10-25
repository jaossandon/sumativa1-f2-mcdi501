"""Sumativa 3 · Punto 1 · Preparación de datos y manejo de faltantes.

Responsable: Fernanda Ovalle Román · MCDI501 · Grupo 6

Este módulo cubre el criterio 1 de la pauta (21 pts):

  1. Resumen del diagnóstico de faltantes de la S1, sin recalcularlo, y
     caracterización del mecanismo de pérdida.
  2. Imputación por regresión lineal múltiple, con verificación de supuestos
     (normalidad de residuos, homocedasticidad, colinealidad) y métricas de
     ajuste (R², RMSE).
  3. Comparación sistemática de las tres estrategias: eliminación de casos,
     imputación simple e imputación por regresión.
  4. Partición entrenamiento/prueba estratificada, con semilla fija.

Requiere: pandas, numpy, scipy, statsmodels, scikit-learn.

    pip install statsmodels scikit-learn
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# ─────────────────────────────────────────────────────────── constantes ──
UMBRAL_ALTO = 4          # atraso alto, tal como se definió en la S1
SEMILLA = 42             # exigida por la pauta
CODIGO_SIN_ANIO = 1900   # centinela de anio_ing_carr_ori
CODIGO_SIN_SEM = 0       # centinela de sem_ing_carr_ori

ARCHIVO_CRUDO = "20260817_Titulados_Ed_Superior_2025_WEB.csv"

# Predictores de la imputación. Cuatro, dentro del rango 3–5 que pide la
# pauta, elegidos por disponibilidad y por las correlaciones de S1/S2.
PREDICTORES_NUM = ["semestres_desde_act", "dur_total_carr", "edad_titulacion"]
PREDICTORES_CAT = ["area_conocimiento"]

OBJETIVO = "semestres_reales"


def _buscar_crudo(ruta: Optional[str]) -> Path:
    """Ubica el CSV crudo sin obligar a una estructura de carpetas concreta."""
    if ruta:
        p = Path(ruta).expanduser()
        if p.exists():
            return p
        raise FileNotFoundError(f"No está {p}")

    aqui = Path(__file__).resolve()
    candidatos = [
        aqui.parents[2] / "data" / "raw" / ARCHIVO_CRUDO,
        aqui.parents[3] / "data" / "raw" / ARCHIVO_CRUDO,
        Path.cwd() / "data" / "raw" / ARCHIVO_CRUDO,
        Path.home() / "Documents" / "proyecto-grupox-mcdi500" / "data" / "raw" / ARCHIVO_CRUDO,
    ]
    for c in candidatos:
        if c.exists():
            return c
    raise FileNotFoundError(
        "No encontré el CSV crudo. Pásalo explícitamente:\n"
        "    cargar_base(ruta='/ruta/al/" + ARCHIVO_CRUDO + "')\n"
        "Probé en:\n  " + "\n  ".join(str(c) for c in candidatos))


# ═══════════════════════════════════════════════════ 1 · carga y derivadas ──
def cargar_base(ruta: Optional[str] = None) -> pd.DataFrame:
    """Reproduce el preprocesamiento de la S1 y agrega las derivadas de la S3.

    Reproduce exactamente la S1: filtra a pregrado universitario, convierte los
    centinelas 1900 y 0 en faltantes, y deriva `semestres_reales`,
    `edad_titulacion` y `atraso_semestres`. Debe dar 105.063 filas, de las
    cuales 91.667 tienen atraso calculable.

    Agrega una derivada propia de la S3: `semestres_desde_act`, la duración
    calculada desde el ingreso a la carrera **actual**, que está observada en
    el 100 % de los casos y es el predictor principal de la imputación.
    """
    crudo = pd.read_csv(_buscar_crudo(ruta), sep=";", encoding="utf-8",
                        low_memory=False)
    df = crudo[(crudo["nivel_global"] == "Pregrado") &
               (crudo["tipo_inst_1"] == "Universidades")].copy()

    # Centinelas → faltantes, conservando la bandera (criterio de la S1)
    df["ingreso_sin_info"] = df["anio_ing_carr_ori"].eq(CODIGO_SIN_ANIO)
    df["anio_ing_carr_ori"] = df["anio_ing_carr_ori"].replace(CODIGO_SIN_ANIO, np.nan)
    df["sem_ing_carr_ori"] = df["sem_ing_carr_ori"].replace(CODIGO_SIN_SEM, np.nan)

    # Índice de semestre: dos por año, para poder restar
    anio_tit = df["fecha_obtencion_titulo"] // 10000
    mes_tit = (df["fecha_obtencion_titulo"] // 100) % 100
    sem_tit = np.where(mes_tit <= 6, 1, 2)
    idx_titulo = anio_tit * 2 + (sem_tit - 1)

    idx_ori = df["anio_ing_carr_ori"] * 2 + (df["sem_ing_carr_ori"] - 1)
    idx_act = df["anio_ing_carr_act"] * 2 + (df["sem_ing_carr_act"] - 1)

    df["semestres_reales"] = idx_titulo - idx_ori + 1
    df["semestres_desde_act"] = idx_titulo - idx_act + 1

    anio_nac = df["fec_nac_alu"] // 100
    mes_nac = df["fec_nac_alu"] % 100
    df["edad_titulacion"] = ((anio_tit * 12 + mes_tit) - (anio_nac * 12 + mes_nac)) / 12

    df["atraso_semestres"] = df["semestres_reales"] - df["dur_total_carr"]
    df["atraso_alto"] = (df["atraso_semestres"] > UMBRAL_ALTO).astype("Int64")
    df.loc[df["atraso_semestres"].isna(), "atraso_alto"] = pd.NA

    return df.reset_index(drop=True)


# ═════════════════════════════════════════════ 2 · diagnóstico de faltantes ──
def diagnostico_faltantes(df: pd.DataFrame) -> Dict[str, object]:
    """Resume el diagnóstico de la S1 y caracteriza el mecanismo de pérdida.

    La pauta pide resumir sin recalcular. El resumen se acompaña de la única
    comprobación que permite nombrar el mecanismo: si la ausencia depende de
    variables observadas, el mecanismo es MAR y no MCAR, y eso habilita la
    imputación condicional.
    """
    n = len(df)
    falta = df["ingreso_sin_info"]

    resumen = pd.DataFrame([
        ["anio_ing_carr_ori", f"centinela {CODIGO_SIN_ANIO}", int(falta.sum()),
         round(100 * falta.mean(), 2)],
        ["sem_ing_carr_ori", f"centinela {CODIGO_SIN_SEM}",
         int(df["sem_ing_carr_ori"].isna().sum()),
         round(100 * df["sem_ing_carr_ori"].isna().mean(), 2)],
        ["semestres_reales", "derivada de las anteriores",
         int(df["semestres_reales"].isna().sum()),
         round(100 * df["semestres_reales"].isna().mean(), 2)],
        ["atraso_semestres", "derivada de las anteriores",
         int(df["atraso_semestres"].isna().sum()),
         round(100 * df["atraso_semestres"].isna().mean(), 2)],
    ], columns=["variable", "origen del faltante", "casos", "% del total"])

    # ¿La ausencia depende de variables observadas?
    por_jornada = (df.groupby("jornada", observed=True)["ingreso_sin_info"]
                     .agg(n="size", pct_sin_info=lambda s: round(100 * s.mean(), 1))
                     .sort_values("pct_sin_info", ascending=False)
                     .reset_index())

    razon = (por_jornada["pct_sin_info"].max() /
             max(por_jornada["pct_sin_info"].min(), 0.01))

    return {
        "n_total": n,
        "n_faltantes": int(falta.sum()),
        "n_completos": int(df["atraso_semestres"].notna().sum()),
        "resumen": resumen,
        "por_jornada": por_jornada,
        "razon_max_min": round(razon, 1),
        "mecanismo": "MAR" if razon > 3 else "compatible con MCAR",
    }


# ═══════════════════════════════════════════ 3 · imputación por regresión ──
def _matriz(df: pd.DataFrame) -> pd.DataFrame:
    """Matriz de diseño: numéricas tal cual, categóricas en indicadoras."""
    X = df[PREDICTORES_NUM].copy()
    for c in PREDICTORES_CAT:
        ind = pd.get_dummies(df[c].astype("object"), prefix=c, drop_first=True,
                             dtype=float)
        X = pd.concat([X, ind], axis=1)
    return X


def ajustar_imputador(df: pd.DataFrame) -> Dict[str, object]:
    """Ajusta la regresión lineal múltiple sobre las observaciones completas.

    Devuelve el modelo, las métricas de ajuste y el resultado de los tres
    supuestos que pide la pauta.
    """
    import statsmodels.api as sm

    completo = df[df[OBJETIVO].notna()].copy()
    X = _matriz(completo)
    y = completo[OBJETIVO].astype(float)

    valido = X.notna().all(axis=1) & y.notna()
    X, y = X[valido], y[valido]

    modelo = sm.OLS(y, sm.add_constant(X, has_constant="add")).fit()
    pred = modelo.fittedvalues
    resid = y - pred

    return {
        "modelo": modelo,
        "n_ajuste": int(len(y)),
        "predictores": list(X.columns),
        "r2": float(modelo.rsquared),
        "r2_aj": float(modelo.rsquared_adj),
        "rmse": float(np.sqrt(np.mean(resid ** 2))),
        "mae": float(np.mean(np.abs(resid))),
        "supuestos": verificar_supuestos(modelo, X, resid),
        "coeficientes": pd.DataFrame({
            "coef": modelo.params, "ee": modelo.bse,
            "t": modelo.tvalues, "p": modelo.pvalues,
        }).round(4),
    }


def verificar_supuestos(modelo, X: pd.DataFrame, resid: pd.Series) -> pd.DataFrame:
    """Normalidad de los residuos, homocedasticidad y colinealidad.

    Con n del orden de 90.000, las pruebas formales de normalidad y de
    homocedasticidad rechazan casi siempre: detectan desviaciones irrelevantes.
    Por eso se informa el estadístico junto con una medida de magnitud, y el
    veredicto se apoya en la magnitud, no en el valor p.
    """
    from scipy import stats
    from statsmodels.stats.diagnostic import het_breuschpagan
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    filas = []

    # Normalidad: asimetría y curtosis, que son interpretables en magnitud
    asim, curt = float(stats.skew(resid)), float(stats.kurtosis(resid))
    filas.append(["Normalidad de residuos", f"asimetría {asim:.2f}, curtosis {curt:.2f}",
                  "aceptable" if abs(asim) < 2 and abs(curt) < 7 else "se aparta"])

    # Homocedasticidad: Breusch-Pagan
    Xc = np.column_stack([np.ones(len(X)), X.values.astype(float)])
    lm, p_lm, _, _ = het_breuschpagan(resid, Xc)
    filas.append(["Homocedasticidad (Breusch-Pagan)", f"LM {lm:.1f}, p {p_lm:.3g}",
                  "homocedástico" if p_lm > 0.05 else "heterocedástico"])

    # Colinealidad: VIF
    vifs = []
    Xn = X.loc[:, X.std() > 0].astype(float)
    Xv = np.column_stack([np.ones(len(Xn)), Xn.values])
    for i, c in enumerate(Xn.columns, start=1):
        try:
            vifs.append((c, variance_inflation_factor(Xv, i)))
        except Exception:
            pass
    peor = max(vifs, key=lambda t: t[1]) if vifs else ("—", float("nan"))
    filas.append(["Colinealidad (VIF máximo)", f"{peor[0]} = {peor[1]:.2f}",
                  "sin colinealidad" if peor[1] < 5 else "colinealidad alta"])

    tabla = pd.DataFrame(filas, columns=["Supuesto", "Estadístico", "Veredicto"])
    tabla.attrs["vif"] = pd.DataFrame(vifs, columns=["variable", "VIF"]).round(2)
    return tabla


# ═══════════════════════════════════════════════ 4 · las tres estrategias ──
def estrategia_eliminacion(df: pd.DataFrame) -> pd.DataFrame:
    """E1 · Análisis de casos completos (listwise deletion)."""
    out = df[df[OBJETIVO].notna()].copy()
    out.attrs["estrategia"] = "Eliminación de casos"
    return out


def estrategia_simple(df: pd.DataFrame, medida: str = "mediana") -> pd.DataFrame:
    """E2 · Imputación simple por la mediana (o la media) de la variable."""
    out = df.copy()
    valor = (out[OBJETIVO].median() if medida == "mediana" else out[OBJETIVO].mean())
    out[OBJETIVO] = out[OBJETIVO].fillna(valor)
    out["atraso_semestres"] = out[OBJETIVO] - out["dur_total_carr"]
    out["atraso_alto"] = (out["atraso_semestres"] > UMBRAL_ALTO).astype("Int64")
    out.attrs["estrategia"] = f"Imputación simple ({medida} = {valor:.1f})"
    return out


def estrategia_regresion(df: pd.DataFrame, ajuste: Dict[str, object]) -> pd.DataFrame:
    """E3 · Imputación por regresión lineal múltiple."""
    import statsmodels.api as sm

    out = df.copy()
    falta = out[OBJETIVO].isna()

    X = _matriz(out)
    # Las indicadoras que el modelo no vio se descartan; las que faltan, a 0
    for c in ajuste["predictores"]:
        if c not in X.columns:
            X[c] = 0.0
    X = X[ajuste["predictores"]]

    utilizable = falta & X.notna().all(axis=1)
    pred = ajuste["modelo"].predict(sm.add_constant(X[utilizable], has_constant="add"))

    # La duración en semestres es un conteo: se redondea y se acota a >= 1
    out.loc[utilizable, OBJETIVO] = np.maximum(np.round(pred), 1)
    out["atraso_semestres"] = out[OBJETIVO] - out["dur_total_carr"]
    out["atraso_alto"] = (out["atraso_semestres"] > UMBRAL_ALTO).astype("Int64")

    out.attrs["estrategia"] = "Imputación por regresión"
    out.attrs["n_imputados"] = int(utilizable.sum())
    out.attrs["n_sin_imputar"] = int((falta & ~utilizable).sum())
    return out


def comparar_estrategias(conjuntos: Dict[str, pd.DataFrame],
                         referencia: str = "Eliminación") -> pd.DataFrame:
    """Compara n, media, desviación, asimetría y las correlaciones de S1/S2."""
    from scipy import stats

    pares = [("atraso_semestres", "edad_titulacion"),
             ("semestres_reales", "edad_titulacion"),
             ("dur_total_carr", "atraso_semestres")]

    filas = []
    for nombre, d in conjuntos.items():
        s = d["atraso_semestres"].dropna()
        fila = {
            "Estrategia": nombre,
            "n": len(d),
            "n con atraso": int(d["atraso_semestres"].notna().sum()),
            "media": round(s.mean(), 3),
            "desv.": round(s.std(), 3),
            "asimetría": round(float(stats.skew(s)), 3),
            "% atraso alto": round(100 * (s > UMBRAL_ALTO).mean(), 1),
        }
        for a, b in pares:
            sub = d[[a, b]].dropna()
            rho = stats.spearmanr(sub[a], sub[b]).statistic if len(sub) > 2 else np.nan
            fila[f"ρ {a[:12]}–{b[:9]}"] = round(float(rho), 3)
        filas.append(fila)

    return pd.DataFrame(filas)


# ═════════════════════════════════════════════════════ 5 · partición ──
def particion(df: pd.DataFrame, prueba: float = 0.30,
              semilla: int = SEMILLA) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Partición 70/30 estratificada por la variable objetivo.

    La estratificación no es un adorno: `atraso_alto` ronda el 20 %, de modo
    que una partición simple puede dejar proporciones distintas en cada parte
    y hacer que las métricas de prueba no sean comparables con las de ajuste.
    """
    from sklearn.model_selection import train_test_split

    d = df[df["atraso_alto"].notna()].copy()
    tr, te = train_test_split(d, test_size=prueba, random_state=semilla,
                              stratify=d["atraso_alto"].astype(int))
    tr.attrs["parte"], te.attrs["parte"] = "entrenamiento", "prueba"
    return tr.reset_index(drop=True), te.reset_index(drop=True)


def resumen_particion(tr: pd.DataFrame, te: pd.DataFrame) -> pd.DataFrame:
    """Comprueba que la estratificación preservó la proporción."""
    return pd.DataFrame([
        {"Conjunto": "Entrenamiento", "n": len(tr),
         "% del total": round(100 * len(tr) / (len(tr) + len(te)), 1),
         "% atraso alto": round(100 * tr["atraso_alto"].astype(int).mean(), 2)},
        {"Conjunto": "Prueba", "n": len(te),
         "% del total": round(100 * len(te) / (len(tr) + len(te)), 1),
         "% atraso alto": round(100 * te["atraso_alto"].astype(int).mean(), 2)},
    ])
