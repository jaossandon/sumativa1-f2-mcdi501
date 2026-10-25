# Preparación de datos y manejo de faltantes

*Sección para el informe integrado de la Sumativa 3 · Fernanda Ovalle Román*

> **Para quien arme el informe.** Son 1.500 palabras más tres tablas y tres
> figuras: entre tres y cuatro de las diez páginas disponibles. Es demasiado
> si las otras cuatro secciones ocupan lo mismo, así que viene con un orden de
> recorte ya pensado:
>
> 1. El párrafo que acota el alcance de las violaciones de supuestos (§2) se
>    puede reducir a dos líneas.
> 2. La tabla de predictores (§2) cabe en una frase enumerándolos.
> 3. La tabla de faltantes por jornada (§1) se puede sustituir por la figura
>    `s3_01`, que dice lo mismo.
>
> Con esos tres recortes queda en unas dos páginas. **Lo que no se puede
> quitar es la caracterización MAR de §1**: de ella depende toda la
> justificación del conjunto elegido, y sin ese argumento la elección parece
> arbitraria.
>
> Las figuras están en `S3/informe/figuras/`.

---

## 1. Diagnóstico de los valores no observados

La Sumativa 1 identificó que las variables `anio_ing_carr_ori` y
`sem_ing_carr_ori` traen los códigos centinela 1900 y 0 en 13.396 registros,
el 12,75 % de los 105.063 titulados de pregrado universitario. De ellas
depende `semestres_reales`, y de esta `atraso_semestres`, que es la variable
sobre la que se construye el objetivo del modelo logístico. El conjunto con
atraso calculable queda en 91.667 observaciones, cifra sobre la que se
obtuvieron todos los resultados de S1 y S2.

Lo que esta sección agrega al diagnóstico es la caracterización del mecanismo
de pérdida, que la S1 dejó pendiente y que determina qué tratamiento es
admisible. La distinción es operativa, no terminológica: si la ausencia fuera
completamente aleatoria (MCAR), el análisis de casos completos sería
insesgado; si depende de variables observadas (MAR), eliminarlos introduce
sesgo y la imputación condicional pasa a ser el procedimiento correcto.

La comprobación es directa. La proporción de registros sin año de ingreso
original varía sistemáticamente según la jornada:

| Jornada | n | Sin año de ingreso |
|---|---:|---:|
| A Distancia | 9.064 | 75,9 % |
| Semipresencial | 828 | 54,1 % |
| Otra | 543 | 51,6 % |
| Vespertina | 12.431 | 36,9 % |
| Diurna | 82.197 | **1,5 %** |

La razón entre el extremo superior y el inferior es de **50 veces**. El
mecanismo es, por tanto, **MAR**. La consecuencia práctica es que descartar
los casos incompletos no elimina un 12,75 % repartido de manera uniforme:
elimina tres de cada cuatro titulados a distancia y prácticamente ninguno de
la jornada diurna. Dado que la jornada es una de las variables explicativas
previstas para el modelo logístico, ese sesgo de composición se trasladaría
directamente a los coeficientes estimados.

*[Figura: `s3_01_faltantes_por_jornada.png`]*

## 2. Imputación mediante regresión lineal múltiple

Se modela `semestres_reales`, que es la cantidad de la que depende el atraso y
la única cuyo error de ajuste admite lectura directa en semestres.

La viabilidad de la imputación descansa en un hallazgo del propio conjunto de
datos: la variable `anio_ing_carr_act` —año de ingreso a la carrera actual—
está observada en el **100 %** de los 13.396 registros incompletos, y coincide
con el año de ingreso original en el 91,2 % de los registros completos. El
dato ausente es, en buena medida, recuperable desde uno disponible.

Los predictores son cuatro, dentro del rango de tres a cinco que fija la
pauta, seleccionados por disponibilidad completa en los casos a imputar y por
respaldo en las correlaciones de S1 validadas en S2:

| Predictor | Fundamento |
|---|---|
| `semestres_desde_act` | Duración calculada desde el ingreso a la carrera actual; sustituto directo del dato ausente |
| `dur_total_carr` | Duración formal del plan; ρ = 0,46 con los semestres reales (S2) |
| `edad_titulacion` | ρ = 0,47 con el atraso, la correlación más fuerte validada en S2 |
| `area_conocimiento` | La S2 documentó heterogeneidad por área en la brecha de atraso |

El modelo se ajusta sobre las 91.667 observaciones completas y alcanza un
**R² de 0,79**, con **RMSE de 2,31 semestres** y error absoluto medio de
**0,98 semestres**: la imputación típica se desvía en menos de un semestre.

**Verificación de supuestos.** La colinealidad no representa un problema: el
factor de inflación de la varianza máximo es 2,42, con todos los predictores
por debajo de 2,5. Los otros dos supuestos no se satisfacen. Los residuos
presentan asimetría de 7,6 y curtosis de 106, y la prueba de Breusch-Pagan
rechaza la homocedasticidad. El origen es sustantivo: existe un subconjunto de
titulaciones con duraciones muy superiores a las que los predictores
anticipan —trayectorias interrumpidas y retomadas— que un modelo lineal no
reproduce.

El alcance de esas violaciones debe precisarse, porque determina si
comprometen o no el uso que se da al modelo. Ambas afectan a la *inferencia*:
con residuos no normales y varianza no constante, los errores estándar y los
valores p de los coeficientes dejan de ser confiables. Aquí el modelo no se
emplea para inferir sobre sus coeficientes, sino para **predecir** un valor
ausente, y la estimación por mínimos cuadrados conserva la insesgadez y la
consistencia para la media condicional aunque esos supuestos fallen. El
criterio pertinente es el error de predicción, y este se mantiene por debajo
del semestre. La cautela que sí corresponde señalar es que el modelo
subestima las duraciones extremas, de modo que la imputación comprime la cola
derecha de la distribución; el apartado siguiente mide ese efecto en lugar de
suponerlo.

*[Figura: `s3_02_supuestos.png`]*

Se imputaron los **13.396 casos**, la totalidad de los faltantes, sin
registros sin resolver.

## 3. Comparación de las tres estrategias

| Estrategia | n | Media atraso | Desv. | Asimetría | % atraso alto | ρ atraso–edad | ρ dur. formal–atraso |
|---|---:|---:|---:|---:|---:|---:|---:|
| Eliminación de casos | 91.667 | 3,398 | 4,76 | 4,41 | 24,5 | 0,466 | 0,009 |
| Imputación simple | 105.063 | 3,787 | 4,61 | 4,05 | **32,7** | 0,541 | **−0,218** |
| **Imputación por regresión** | 105.063 | **3,400** | 4,53 | 4,55 | 23,8 | 0,468 | −0,069 |

**La imputación simple deforma la distribución.** Eleva la media del atraso de
3,398 a 3,787 e incrementa la proporción de atraso alto de 24,5 % a 32,7 %:
ocho puntos porcentuales sin respaldo empírico. El mecanismo es directo —
asigna la misma duración mediana a todos los casos incompletos, que se
concentran en carreras de duración formal corta, de modo que la diferencia
`semestres_reales − dur_total_carr` produce atrasos artificialmente elevados.

El efecto más grave es que **invierte una conclusión validada en la S2**. La
correlación entre duración formal y atraso pasa de 0,009 —valor que la S2
calificó de estable y de magnitud despreciable, sosteniendo que el atraso no
depende de la extensión de la carrera— a **−0,218**. Un conjunto construido
así respaldaría una afirmación que las dos entregas anteriores descartaron
explícitamente.

**La imputación por regresión preserva los hallazgos.** La media queda en
3,400 frente a 3,398 del conjunto original, la proporción de atraso alto en
23,8 % frente a 24,5 %, y la correlación atraso–edad en 0,468 frente a 0,466.
Recupera las 13.396 observaciones sin desplazar lo establecido en S1 y S2.

**Su limitación, declarada.** La correlación entre semestres reales y edad de
titulación desciende de 0,461 a 0,175. Es el efecto previsible de sustituir
valores observados por predicciones, que presentan menor variabilidad que los
datos originales, y se concentra en la modalidad a distancia, donde se imputan
tres de cada cuatro registros. Toda conclusión referida a esa modalidad debe
declarar que descansa mayoritariamente en valores imputados.

*[Figura: `s3_03_estrategias.png`]*

## 4. Conjunto base y partición

Se adopta el conjunto con **imputación por regresión** como base del
modelamiento logístico, por tres razones en orden de peso:

1. **El mecanismo es MAR.** La eliminación de casos no retira una fracción
   aleatoria sino el 75,9 % de una categoría y el 1,5 % de otra, y la jornada
   es variable explicativa del modelo.
2. **Preserva los resultados de S1 y S2**, mientras que la imputación simple
   invierte uno de ellos.
3. **Recupera 13.396 observaciones** —un 14,6 % adicional— precisamente en las
   categorías con menor respaldo muestral bajo la estrategia de eliminación.

La elección no se da por cerrada: el análisis comparativo del impacto de la
imputación reajusta la especificación final sobre los tres conjuntos y
contrasta coeficientes, amplitud de intervalos, AUC y exactitud, de modo que
la decisión queda sujeta a verificación empírica.

La partición es de 70 % para entrenamiento y 30 % para prueba, con
`random_state = 42`, **estratificada** por la variable objetivo. La
estratificación responde a que `atraso_alto` representa cerca del 24 % de los
casos: una partición simple podría dejar proporciones distintas en cada
subconjunto y hacer que las métricas de prueba no fueran comparables con las
de ajuste. El resultado conserva un 23,84 % de atraso alto en ambas partes.

| Conjunto | n | % del total | % atraso alto |
|---|---:|---:|---:|
| Entrenamiento | 73.544 | 70,0 | 23,84 |
| Prueba | 31.519 | 30,0 | 23,84 |

## 5. Reproducibilidad

Toda la lógica reside en `S3/src/preparacion.py`; el cuaderno
`S3/notebooks/S3_01_Preparacion_Datos.ipynb` la orquesta y documenta. Los
conjuntos derivados no se versionan —son 14 MB regenerables— y se obtienen
ejecutando el cuaderno, que los deposita en `S3/resultados/` en formato
parquet: `e1_eliminacion`, `e2_simple`, `e3_regresion`, `train_e3` y
`test_e3`. La variable objetivo es `atraso_alto` y el conjunto base es
`e3_regresion.parquet`. Dependencias añadidas al proyecto: `statsmodels`,
`scikit-learn` y `pyarrow`.
