# Evaluación Sumativa 3: Modelamiento Predictivo Integrado
**MCDI501: Estadística Computacional para la Toma de Decisiones**  
*Magíster en Ciencia de Datos e Inteligencia Artificial — Universidad Andrés Bello (UNAB)*

---

### Datos del Proyecto
- **Título del proyecto:** Modelamiento Predictivo Integrado del Atraso Académico en Educación Superior
- **Integrantes:**
  - Fernanda Ovalle Román
  - Sebastián Cajales Cid
  - César Lorca Bacián
  - Jorge Álvarez Ossandón
- **Dataset:** Titulados de Educación Superior 2025 – Datos Abiertos Mineduc / SIES ($n = 105.063$)
- **Docente:** Jean Paul Maidana González
- **Fecha:** Octubre 2026
- **Repositorio GitHub:** [jaossandon/sumativa1-f2-mcdi501](https://github.com/jaossandon/sumativa1-f2-mcdi501)

---

## Resumen Ejecutivo

El presente informe consolida el proyecto de modelamiento predictivo sobre la duración real y el atraso académico en la educación universitaria en Chile, utilizando el registro oficial de Titulados de Educación Superior 2025 del Mineduc ($n = 105.063$). El objetivo central es predecir la probabilidad de que un estudiante experimente un **atraso alto** (definido operacionalmente en S1 y S2 como un atraso superior a 4 semestres sobre la duración formal del plan curricular) mediante técnicas de regresión logística, evaluando rigurosamente el impacto del tratamiento de datos faltantes y la estabilidad paramétrica mediante remuestreo bootstrap ($B \ge 1.000$ iteraciones).

La progresión metodológica del estudio integra tres fases complementarias:
1. **Fase 1 (S1):** Diagnóstico exploratorio e inferencial paramétrico, detección de 12,75 % de faltantes administrativos en la cohorte de ingreso y caracterización de variables clave.
2. **Fase 2 (S2):** Validación computacional no paramétrica (Bootstrap percentil y BCa con $B = 10.000$, pruebas de permutación, simulación Monte Carlo de cohortes y Jackknife por institución), demostrando que las correlaciones son estables y que los atípicos afectan la magnitud de colas pero no la dirección de los efectos.
3. **Fase 3 (S3):** Imputación inteligente de datos faltantes mediante regresión múltiple, comparación sistemática con eliminación y media, ajuste de tres especificaciones logísticas (teórica, stepwise e información AIC/BIC), diagnóstico de supuestos (VIF, linealidad, residuos y observaciones influyentes) y evaluación de sensibilidad de la política analítica.

> **[Pendiente ejecución Notebook S3]:** Cifras definitivas de desempeño (AUC-ROC, Accuracy, variables finales de mayor peso Odds Ratio y conclusión de impacto de la imputación).

---

## Introducción y Contexto del Problema

La sobre-duración de los programas de pregrado universitario representa un desafío estructural crítico en el sistema de educación superior chileno, con profundas repercusiones financieras, laborales e institucionales. Tanto los aranceles reales como los costos de oportunidad para los estudiantes se incrementan sustantivamente ante cada semestre de retraso, mientras que las instituciones enfrentan restricciones asociadas a las políticas de gratuidad y a los criterios de acreditación de la Comisión Nacional de Acreditación (CNA).

En la Sumativa 1 se identificó que la duración formal de las carreras no refleja la trayectoria efectiva de titulación: el atraso medio asciende a 3,40 semestres ($IC_{95\%} [3,37; 3,43]$), con una marcada asimetría positiva (mediana de 2 semestres) y una brecha sistemática desfavorable para los hombres ($+1,07$ semestres) y estudiantes de jornadas vespertinas. En la Sumativa 2 se demostró que esta brecha se reduce a la mitad ($0,55$ semestres) al controlar por área de conocimiento (dado que los hombres se concentran en carreras tecnológicas y de ingeniería con duraciones intrínsecamente más largas) y que existe dependencia jerárquica por institución educativa (error estándar Jackknife 3,5 veces superior al de Welch). 

Con estos antecedentes consolidados, la Sumativa 3 aborda la formalización de un modelo predictivo supervisado que permita anticipar tempranamente el riesgo de rezago severo, garantizando a la vez la robustez de las inferencias ante diferentes decisiones de preprocesamiento de datos.

---

## 1. Manejo Inteligente de Datos Faltantes (21 pts)

### 1.1 Referencia al análisis de faltantes de S1
En la Sumativa 1, sobre un total de 105.063 titulados de pregrado universitario, se identificó que las variables `anio_ing_carr_ori` y `sem_ing_carr_ori` contenían valores artificiales de relleno administrativo codificados originalmente como `1900` y `0`, respectivamente. Dicha condición afectó exactamente a $13.396$ observaciones, equivalentes al **12,75 %** del universo analizado. Al convertir estos códigos a `NaN`, fue imposible calcular de manera directa las variables derivadas `semestres_reales` y `atraso_semestres` para dichos individuos, reduciendo la muestra completa a $n = 91.667$.

Conforme a la taxonomía de Little y Rubin (2019), el mecanismo generador de pérdida no es *Missing Completely at Random* (MCAR), dado que la probabilidad de ausencia de información histórica no es homogénea entre programas ni instituciones. En S1 se caracterizó este patrón como **Missing at Random (MAR)**, puesto que la no observación de la fecha de ingreso original está correlacionada con variables institucionales y académicas observables: tipos específicos de institución, procesos de convalidación externa y programas especiales en jornada vespertina. Dado que el mecanismo es MAR condicionado a variables del registro curricular, la eliminación de casos completos (*complete-case analysis*) introduce sesgos potenciales de selección, justificando plenamente el uso de métodos de imputación basados en información auxiliar observada.

### 1.2 Imputación mediante regresión lineal múltiple
Para imputar el tiempo efectivo de egreso y recuperar los $13.396$ casos incompletos, se modela la variable continua `semestres_reales` a partir de los predictores que mostraron las correlaciones más intensas y robustas en S1, ratificadas como altamente estables mediante remuestreo bootstrap en S2:
1. `edad_titulacion`: Correlación lineal positiva moderada-fuerte ($\rho = 0,466$, $IC_{95\%} [0,460; 0,472]$), validada con error estándar mínimo ($EE = 0,003$).
2. `dur_total_carr`: Duración formal del plan curricular, con correlación teórica inversa respecto a la edad de ingreso y directa respecto al ciclo formativo.
3. `area_conocimiento`: Efecto fijo por disciplina académica (particularmente Tecnología, Ciencias Básicas y Salud).
4. `jornada`: Diferencial estructural diurno versus vespertino (brecha de atraso alto de 9,06 puntos porcentuales validada en S2).

El modelo de imputación se especifica como:
$$\widehat{\text{semestres\_reales}}_i = \beta_0 + \beta_1\,\text{edad\_titulacion}_i + \beta_2\,\text{dur\_total\_carr}_i + \sum_{k} \gamma_k\,\text{Area}_{ik} + \delta\,\text{Vespertino}_i + \varepsilon_i$$

El ajuste se realiza exclusivamente sobre las $91.667$ observaciones con información completa. Los supuestos del modelo de regresión lineal (normalidad asintótica de residuos, homocedasticidad y factor de inflación de varianza $VIF < 5$) son evaluados previo a la imputación.

| Variable Objetivo | Predictores Clave | $R^2$ | RMSE | Casos Imputados |
|---|---|:---:|:---:|:---:|
| `semestres_reales` | Edad titulación, Duración formal, Área, Jornada | *[Pendiente]* | *[Pendiente]* | 13.396 |

### 1.3 Comparación de estrategias de imputación
Se contrastan tres estrategias operacionales para el tratamiento de los datos no observados:
- **Estrategia 1 (Eliminación / Complete-Case):** Exclusión listwise de las $13.396$ filas sin fecha de ingreso ($n = 91.667$).
- **Estrategia 2 (Imputación Simple):** Asignación de la media o mediana condicionada a la duración formal ($n = 105.063$).
- **Estrategia 3 (Regresión Lineal Múltiple):** Predicción preservando la covarianza multivariada ($n = 105.063$).

| Estrategia | $n$ | Media | Desv. Est. | Asimetría | $\text{Corr}(\text{atraso, edad})$ |
|---|:---:|:---:|:---:|:---:|:---:|
| 1. Eliminación (Complete-case) | 91.667 | 3,40 | 4,51 | Positiva | 0,466 |
| 2. Imputación simple (mediana) | 105.063 | *[Pendiente]* | *[Pendiente]* | *[Pendiente]* | *[Pendiente]* |
| 3. Imputación regresión lineal | 105.063 | *[Pendiente]* | *[Pendiente]* | *[Pendiente]* | *[Pendiente]* |

**Justificación de la base para modelamiento:** *[Pendiente confirmación numérica: justificar la elección del dataset en base a la no distorsión de la varianza y la preservación de la estructura de covarianza validada en S2].*

---

## 2. Clasificación mediante Regresión Logística (60 pts)

### 2.1 Preparación de datos informada por S1
- **Variable objetivo:** Se define la variable dicotómica $Y = \text{atraso\_alto}$, donde $Y_i = 1$ si $\text{atraso\_semestres}_i > 4$, y $0$ en caso contrario, operacionalizando el atraso severo identificado en S1 y S2.
- **Partición de datos:** Partición 70 % para entrenamiento y 30 % para prueba, estratificada por la variable objetivo con semilla fijada en `random_state = 42`.
- **Tratamiento de outliers:** En S1 se identificaron $13.201$ observaciones atípicas según el criterio de Tukey ($1,5 \times IQR$). No obstante, el análisis de robustez de S2 demostró que dichos puntos reflejan rezagos extremos reales de trayectorias formativas complejas y que su exclusión altera la magnitud de las colas pero preserva intacto el signo y la dirección de las asociaciones. En consecuencia, se retienen en el análisis para no perder validez ecológica.
- **Estandarización y codificación:** Variables continuas (`edad_titulacion`, `dur_total_carr`) se escalan a media 0 y varianza unitaria (StandardScaler). Las variables categóricas (`sexo`, `jornada`, `area_conocimiento`) se transforman mediante codificación One-Hot, omitiendo la categoría de referencia para prevenir multicolinealidad perfecta.

### 2.2 Selección de variables informada por S1 y S2
Se evalúan tres especificaciones alternativas de la probabilidad $\pi_i = P(Y_i = 1 \mid \mathbf{x}_i)$:
$$\text{Logit}(\pi_i) = \ln\left(\frac{\pi_i}{1 - \pi_i}\right) = \mathbf{x}_i^T \boldsymbol{\beta}$$

1. **Modelo 1 (Teórico S1/S2):** Especificación fundamentada sustantivamente. Incluye sexo, jornada, área de conocimiento y edad de titulación, reflejando el control por área sugerido en S2 para aislar el efecto de género y el impacto de la jornada vespertina.
2. **Modelo 2 (Stepwise):** Selección iterativa paso a paso basada en el test de razón de verosimilitud ($p < 0,05$).
3. **Modelo 3 (Criterios de Información):** Selección guiada por la minimización del AIC y BIC.

| Modelo / Covariable | $\beta$ | EE | Valor $p$ | Odds Ratio ($e^\beta$) | IC 95 % (OR) | AIC / BIC |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Modelo 1 (Teórico S1/S2)** | | | | | | *[Pendiente]* |
| Intercepto | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | |
| Sexo (Hombre) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | |
| Jornada (Vespertina) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | |
| Edad de titulación | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | |
| Áreas de conocimiento | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | |
| **Modelo 2 (Stepwise)** | \multicolumn{5}{c}{*[Resumen variables seleccionadas y significancia]*} | *[Pendiente]* |
| **Modelo 3 (Criterios Inf.)** | \multicolumn{5}{c}{*[Resumen variables seleccionadas y significancia]*} | *[Pendiente]* |

### 2.3 Evaluación de estabilidad mediante bootstrap (30 pts)
Para evaluar si los coeficientes estimados sufren de inestabilidad o sesgo asintótico debido a la sobredispersión o agrupamiento institucional detectado en S2, se aplica remuestreo bootstrap no paramétrico con $B \ge 1.000$ réplicas sobre el conjunto de entrenamiento:
$$\boldsymbol{\beta}^{*(b)} \sim \text{Logit}(\mathbf{X}^{*(b)}, \mathbf{y}^{*(b)}), \quad b = 1, \dots, B$$

Se calculan los intervalos de confianza empíricos al 95 % (método percentil y BCa) para cada $\beta_j$ y cada Odds Ratio $e^{\beta_j}$, y se contrastan con los intervalos asintóticos tradicionales de Wald ($\widehat{\beta}_j \pm 1,96\,\text{EE}(\widehat{\beta}_j)$).

| Parámetro | $e^{\widehat{\beta}}$ | IC 95 % Wald | IC 95 % Bootstrap | Evaluación Estabilidad |
|---|:---:|:---:|:---:|:---:|
| Sexo (Hombre) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Robusto / Inestable]* |
| Jornada (Vespertina) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Robusto / Inestable]* |
| Edad titulación | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Robusto / Inestable]* |
| Tecnología / Ingeniería | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Robusto / Inestable]* |
| Salud | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Robusto / Inestable]* |

### 2.4 Diagnóstico de supuestos
- **Multicolinealidad (VIF):** Se computa el Factor de Inflación de la Varianza sobre las variables independientes para verificar la ausencia de redundancia severa ($VIF < 5$).
- **Linealidad en el logit (Box-Tidwell):** Se evalúa la linealidad de las covariables continuas (`edad_titulacion`) contrastando el término $X \ln(X)$.
- **Observaciones influyentes:** Se calculan la Distancia de Cook y apalancamientos (*leverage*) para detectar casos que distorsionen los parámetros.
- **Residuos Deviance y Pearson:** Examen de los residuos deviance para contrastar la bondad de ajuste del modelo.

### 2.5 Evaluación de desempeño predictivo
| Modelo / Partición | Accuracy | Precision | Recall | F1-Score | AUC-ROC | Brier Score |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Modelo 1 (Teórico) - Train** | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* |
| **Modelo 1 (Teórico) - Test** | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* |
| **Modelo 2 (Stepwise) - Test** | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* |
| **Modelo 3 (AIC/BIC) - Test** | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Pend.]* |

**Modelo final seleccionado:** *[Pendiente: Declaración formal y justificación del modelo ganador considerando parsimonia, interpretabilidad de negocio y AUC-ROC en Test].*

---

## 3. Análisis Comparativo del Impacto de la Imputación (9 pts)

Para responder a la pregunta analítica central sobre si la técnica de manejo de datos faltantes altera las decisiones institucionales, se re-ajusta la especificación final del modelo logístico de manera idéntica sobre los tres datasets preparados en la Parte 1.

| Métrica / Parámetro | 1. Eliminación | 2. Imp. Simple | 3. Imp. Regresión | Impacto Decisión |
|---|:---:|:---:|:---:|:---:|
| Tamaño muestral ($n$) | 91.667 | 105.063 | 105.063 | Pérdida de 12,75 % |
| $\beta_{\text{sexo(hombre)}}$ | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Estable/Cambia]* |
| IC 95 % $\beta_{\text{sexo}}$ | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Amplitud]* |
| $\beta_{\text{jornada(vesp)}}$ | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Estable/Cambia]* |
| $\beta_{\text{edad\_titulacion}}$ | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Estable/Cambia]* |
| Accuracy (Test) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Variación]* |
| AUC-ROC (Test) | *[Pend.]* | *[Pend.]* | *[Pend.]* | *[Variación]* |

**Conclusión de negocio:** *[Pendiente: Discutir si la imputación por regresión modifica sustantivamente los Odds Ratios o la jerarquía de factores de riesgo respecto al complete-case analysis].*

---

## 4. Discusión y Recomendaciones para la Toma de Decisiones

### 4.1 Integración de la cadena metodológica $S_1 \to S_2 \to S_3$
La fortaleza central de este estudio radica en su estricta coherencia acumulativa:
- En **S1**, la inspección de datos evitó el descarte apresurado de atípicos y aisló la no-respuesta administrativa (12,75 %), alertando sobre la asimetría del atraso.
- En **S2**, la inferencia clásica fue contrastada con métodos de remuestreo, evidenciando que las correlaciones entre atraso, duración formal y edad eran auténticamente lineales y estables, pero advirtiendo que los titulados no son independientes entre universidades (efecto agrupamiento institucional vía Jackknife).
- En **S3**, estos hallazgos guiaron una imputación multivariada no ingenua y permitieron contrastar la inferencia asintótica con bootstrap en la regresión logística, garantizando que los coeficientes y Odds Ratios utilizados para políticas institucionales no sean artefactos de supuestos no verificados.

### 4.2 Recomendaciones para la gestión institucional
1. **Sistemas de Alerta Temprana Diferenciados por Área:** Dado que el efecto del género está fuertemente mediado por el área de conocimiento (demostrado en S2 y modelado en S3), los planes de retención y apoyo académico deben focalizarse en facultades de Ingeniería y Tecnología, con especial monitoreo en programas vespertinos.
2. **Ajuste de Políticas de Financiamiento y Gratuidad:** La alta concentración de estudiantes que superan los 4 semestres de rezago sugiere que los plazos de financiamiento deben considerar mecanismos de flexibilización curricular para evitar el sobreendeudamiento y la deserción de último año.

---

## 5. Presentación del Proyecto y Repositorio (9 pts)

### 5.1 Estructura y distribución del video grupal (10 minutos)
La exposición audiovisual se organiza en cuatro bloques equitativos de 2,5 minutos:
1. **Bloque 1 – Fernanda Ovalle:** Contexto del pregrado universitario chileno, planteamiento del problema de sobre-duración y hallazgos clave de calidad de datos en S1.
2. **Bloque 2 – Jorge Álvarez:** Metodología computacional de validación en S2 (Bootstrap BCa, simulación Monte Carlo de cohortes y análisis Jackknife de dependencia institucional).
3. **Bloque 3 – César Lorca:** Manejo inteligente de datos faltantes, comparación de estrategias de imputación y ajuste de especificaciones de regresión logística en S3.
4. **Bloque 4 – Sebastián Cajales:** Diagnóstico de estabilidad bootstrap del modelo final, evaluación comparativa del impacto de la imputación y recomendaciones estratégicas de negocio.

### 5.2 Trazabilidad y reproducibilidad en GitHub
El repositorio oficial del proyecto ([jaossandon/sumativa1-f2-mcdi501](https://github.com/jaossandon/sumativa1-f2-mcdi501)) conserva la trazabilidad completa y reproducible de todas las etapas del magíster:
- `S1/`: Notebook de análisis exploratorio e inferencial y reporte técnico S1.
- `S2/`: Notebook ejecutado, informe PDF y archivo de resultados validados (`resultados_validados.csv` y `.md`).
- `S3/`: Notebook maestro de modelamiento integrado (`Sumativa3_F4_Titulados.ipynb`) e informe final PDF en plantilla institucional.

---

## 6. Bibliografía (APA 7.ª edición)

- Centro de Estudios Mineduc. (2025). *Base de datos oficial de Titulados en Educación Superior 2025*. Servicio de Información de Educación Superior (SIES). Ministerio de Educación de Chile. https://datosabiertos.mineduc.cl
- Davison, A. C., & Hinkley, D. V. (1997). *Bootstrap methods and their application*. Cambridge University Press.
- Efron, B., & Tibshirani, R. J. (1994). *An introduction to the bootstrap*. CRC press.
- Fox, J., & Weisberg, S. (2019). *An R companion to applied regression* (3.ª ed.). SAGE Publications.
- Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied logistic regression* (3.ª ed.). John Wiley & Sons.
- Little, R. J., & Rubin, D. B. (2019). *Statistical analysis with missing data* (3.ª ed.). John Wiley & Sons.
- Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M., & Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
- van Buuren, S. (2018). *Flexible imputation of missing data* (2.ª ed.). CRC press.
