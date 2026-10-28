# Duración de la titulación en el pregrado universitario chileno (2025)

**Curso:** MCDI501 Estadística Computacional para la Toma de Decisiones  
**Evaluaciones:** Sumativa 1, Fase 2 (carpeta `S1/`) · Sumativa 2, Fase 3 (carpeta `S2/`)  
**Docente:** Jean Paul Maidana González

## Integrantes
- Fernanda Ovalle Román
- Sebastián Cajales Cid
- César Lorca Bacián
- Jorge Álvarez Ossandón

## Pregunta
¿Cuánto se aparta la duración real de las carreras de su duración formal, y difiere ese atraso según sexo y jornada?

## Datos y Descarga Pública (Reproducibilidad)
La investigación se fundamenta en la **Base Oficial de Titulados en Educación Superior 2025**, elaborada por el Servicio de Información de Educación Superior (SIES) del Ministerio de Educación de Chile (Mineduc).

* **Portal oficial de descarga pública:** [Datos Abiertos Mineduc](https://datosabiertos.mineduc.cl)
* **Conjunto de datos:** *Educación Superior - Titulados en Educación Superior 2025*
* **Nombre exacto del archivo descargado:** `20260817_Titulados_Ed_Superior_2025_WEB.csv` (formato CSV delimitado por punto y coma, codificación `latin-1` / `utf-8`).
* **Instrucciones de instalación:**
  1. Descargar el archivo desde el portal oficial [datosabiertos.mineduc.cl](https://datosabiertos.mineduc.cl).
  2. Guardar el archivo directamente en la ruta: `data/raw/20260817_Titulados_Ed_Superior_2025_WEB.csv`
  3. Los scripts y cuadernos aplican automáticamente el filtro metodológico oficial a **Pregrado Universitario** (`nivel_global == 'Pregrado'` y `tipo_inst_1 == 'Universidades'`), obteniendo el universo de **105.063 registros** analizados en las Evaluaciones S1, S2, Formativa 2 y S3.

## Estructura
```
data/raw/                 archivo crudo (no versionado), compartido por S1 y S2
S1/notebooks/             Sumativa1_F2_Titulados.ipynb (Sumativa 1, Fase 2)
S1/informe/               Informe_Sumativa1_F2.pdf y figuras/
S2/notebooks/             notebook de la Sumativa 2, Fase 3
S2/informe/               informe de la Sumativa 2 y figuras/
S2/resultados/            resultados validados (insumo para la Sumativa 3)
requirements.txt          librerías y versiones
```
## Cómo reproducir
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
Luego abrir `S1/notebooks/Sumativa1_F2_Titulados.ipynb` (o el notebook de `S2/notebooks/`) y ejecutar todas las celdas en orden. Los procedimientos aleatorios usan semilla 42.

## Contenido del análisis
1. Preparación y calidad de datos: filtro, faltantes, variables derivadas (`semestres_reales`, `atraso_semestres`, `edad_titulacion`), atípicos marcados sin eliminar.
2. Análisis exploratorio: descriptivos, frecuencias, correlaciones de Spearman y comparación por grupos.
3. Estimación: IC 95 % *t* para la media y bootstrap para la mediana.
4. Pruebas de hipótesis: *t* de Welch (atraso por sexo) y chi-cuadrado (jornada × atraso alto), con tamaño de efecto.

## Resultados principales
- El titulado típico egresa con **2 semestres de atraso** (media 3,40; IC 95 % [3,37; 3,43]).
- Los hombres se atrasan **1,07 semestres más** que las mujeres (*p* < 0,001; *d* = 0,23, efecto pequeño).
- La jornada vespertina tiene **9 puntos porcentuales más** de atraso alto que la diurna (*p* < 0,001; V de Cramér = 0,06).

## Sumativa 2: validación computacional (carpeta `S2/`)
Notebook `S2/notebooks/Sumativa2_F3_Titulados.ipynb` e informe `S2/informe/Informe_Sumativa2_F3.pdf`. Semilla 42, B = R = 10.000.
1. Bootstrap (percentil y BCa) de 3 intervalos de confianza.
2. Pruebas de permutación de las dos pruebas de la S1.
3. Estabilidad bootstrap de 4 correlaciones de Spearman.
4. Simulación Monte Carlo (binomial negativa con parámetros de la S1): potencia según tamaño de cohorte y convergencia.
5. Robustez: atípicos, medias recortadas, jackknife por institución, umbrales, distribuciones y efecto del área.
6. Resultados validados para la S3 en `S2/resultados/` (`resultados_validados.csv` y `.md`).

**Hallazgos:** los IC y las pruebas de la S1 se validan. La brecha por sexo es robusta en el signo pero no en la magnitud: la mitad se explica por el área de conocimiento (0,55 semestres dentro de áreas), y el EE por institución es 3,5 veces el de Welch. En cohortes de menos de ~700 titulados la brecha no es detectable.