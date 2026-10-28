# Evaluación Sumativa 3: Cierre y Comunicación
## Modelamiento Predictivo Integrado del Atraso Académico en Educación Superior
**Magíster en Ciencia de Datos e Inteligencia Artificial**  
*MCDI501: Estadística Computacional para la Toma de Decisiones — Universidad Andrés Bello*  
**Grupo 6:** Fernanda Ovalle Román, Sebastián Cajales Cid, César Lorca Bacián, Jorge Álvarez Ossandón  
**Docente:** Jean Paul Maidana González · **Fecha:** 28 de octubre de 2026  
**Repositorio GitHub Oficial:** [https://github.com/jaossandon/sumativa1-f2-mcdi501](https://github.com/jaossandon/sumativa1-f2-mcdi501)

---

### Resumen Ejecutivo

Este informe consolida el proyecto de modelamiento predictivo sobre la duración real y el atraso académico en la educación universitaria en Chile, utilizando el registro oficial de Titulados de Educación Superior 2025 del Mineduc ($N = 105.063$). El objetivo central es predecir la probabilidad de que un estudiante experimente un **atraso alto** (definido operacionalmente en S1 y S2 como un rezago superior a 4 semestres sobre la duración formal del plan curricular) mediante regresión logística supervisada, contrastando empíricamente el impacto del tratamiento de datos no observados y la estabilidad de la inferencia mediante remuestreo bootstrap ($B = 1.000$ réplicas) e imputación múltiple congeniada.

#### Aportes y Hallazgos Clave:
1. **Mecanismo MAR y fracaso de la imputación simple:** Los 13.396 registros con fecha de ingreso administrativo no informada (12,75 %) siguen un patrón *Missing at Random* (MAR) condicionado a la modalidad de estudio (A Distancia tiene 75,9 % de no-observación frente a 1,5 % en Diurna; razón de disparidad de 50:1). La imputación simple por mediana ($E_2$) es inadmisible: invierte el signo de 3 jornadas y de Educación, inflando artificialmente la tasa de atraso alto de 24,5 % a 32,7 %.
2. **Modelo logístico óptimo ($M_2$):** La especificación que incorpora Sexo, Área de conocimiento, Jornada y Edad de ingreso minimiza los criterios de información ($	ext{AIC} = 75.421,2$; $	ext{BIC} = 75.568,5$). En la prueba común observada ($n=27.508$), alcanza un $	ext{AUC} = 0,662$ y una exactitud de $65,3\,\%$ (umbral de Youden $= 0,2246$, sensibilidad $= 57,7\,\%$, especificidad $= 67,8\,\%$).
3. **Factores de riesgo estructurales:** Ser mujer reduce el riesgo de atraso severo ($	ext{OR} = 0,75$; IC 95 % $[0,72; 0,78]$), mientras que cursar Derecho ($	ext{OR} = 4,42$), Agropecuaria ($	ext{OR} = 2,42$), Tecnología e Ingeniería ($	ext{OR} = 2,14$) y Ciencias Básicas ($	ext{OR} = 2,03$) lo incrementa sustancialmente.
4. **Dominancia de la heterogeneidad institucional:** El remuestreo bootstrap ($B=1.000$) y el análisis clúster por universidad demuestran que los errores estándar se ensanchan entre 3,5 y 9,2 veces respecto a la inferencia asintótica de Wald, confirmando el hallazgo de Jackknife de la Sumativa 2: la incertidumbre contextual domina ampliamente sobre la del remuestreo.
5. **Corrección mediante Imputación Múltiple Congeniada (MI):** Se identificó que la imputación por regresión ($E_3$) distorsionó los odds ratios de jornada al omitir dicha covariable en su modelo lineal (asignando un atraso plano de $pprox 20\,\%$). La corrección mediante Imputación Múltiple ($m=20$, reglas de Rubin) redujo la discrepancia media con casos completos del 18,5 % al 7,3 %, calibrando plenamente las probabilidades predichas.

---

## 1. Manejo Inteligente de Datos Faltantes (Parte 1)

### 1.1 Diagnóstico del Mecanismo de Pérdida
En la Sumativa 1 se constató que las variables `anio_ing_carr_ori` y `sem_ing_carr_ori` traían códigos centinela administrativos (`1900` y `0`) en 13.396 registros (12,75 % de los 105.063 titulados universitarios). Al codificarlos como `NaN`, el subconjunto con atraso directamente computable quedó en $n = 91.667$.

La proporción de casos no observados varía de manera extrema según la jornada del estudiante:
* **A Distancia:** 75,9 % incompletos ($n=9.064$)
* **Semipresencial:** 54,1 % incompletos ($n=828$)
* **Otra:** 51,6 % incompletos ($n=543$)
* **Vespertina:** 36,9 % incompletos ($n=12.431$)
* **Diurna:** 1,5 % incompletos ($n=82.197$)

Dado que la razón de disparidad entre extremos es de 50 a 1, se rechaza categóricamente el supuesto de pérdida completamente al azar (*MCAR*, prueba de Little $p < 0,001$). El mecanismo es **MAR** (*Missing at Random*), fuertemente ligado a programas convalidantes y regímenes flexibles. Por tanto, el descarte de casos completos introduce un sesgo de selección que castiga a las modalidades no tradicionales.

### 1.2 Imputación por Regresión Lineal Múltiple
Aprovechando que `anio_ing_carr_act` está observada en el 100 % de los registros incompletos y coincide en el 91,2 % con el ingreso original en completos, se modeló `semestres_reales` usando 4 predictores validados en S1 y S2: `semestres_desde_act` (sustituto cronológico), `dur_total_carr` ($ho = 0,46$), `edad_titulacion` ($ho = 0,47$) y `area_conocimiento`.

* **Bondad de ajuste:** $R^2 = 0,792$, $	ext{RMSE} = 2,308$ semestres, $	ext{MAE} = 0,98$ semestres.
* **Diagnóstico de colinealidad:** $	ext{VIF} < 2,5$ en todos los predictores.

### 1.3 Comparación de Estrategias Distribucionales

| Estrategia | $n$ | Media | Desv. Est. | Asimetría | % Atraso Alto | $ho(	ext{atraso, edad})$ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$E_1$ · Eliminación (Casos completos)** | 91.667 | 3,40 | 4,76 | 4,41 | 24,5 % | 0,466 |
| **$E_2$ · Imputación simple (Mediana)** | 105.063 | 3,79 | 4,61 | 4,05 | 32,7 % | 0,541 |
| **$E_3$ · Regresión lineal multivariada** | 105.063 | 3,40 | 4,53 | 4,55 | 23,8 % | 0,468 |

*Justificación:* $E_2$ distorsiona gravemente la distribución, inflando el rezago alto en 8,2 puntos porcentuales e introduciendo correlación espuria negativa con la duración formal ($ho = -0,218$). En contraste, $E_3$ preserva de manera fiel los cuatro primeros momentos y la estructura de covariación observada.

---

## 2. Clasificación mediante Regresión Logística Supervisada (Parte 2)

### 2.1 Preparación de Datos y Tratamiento de Outliers
* **Variable objetivo:** Binaria $Y_i = \mathbb{I}(	exttt{atraso\_semestres}_i > 4)$, reflejando el rezago crítico definido en S1.
* **Partición de datos:** 70 % train ($n=73.544$) y 30 % test ($n=31.519$), estratificada por $Y$ con semilla 42.
* **Retención de atípicos de S1:** Los 3.201 casos atípicos detectados por criterio Tukey en S1 se retienen en el análisis, ya que la evaluación de robustez de S2 demostró que reflejan rezagos extremos reales cuya omisión artificial sesga la variabilidad sin cambiar los signos.
* **Estandarización y codificación:** One-Hot Encoding para variables categóricas (categorías de referencia: *Hombre*, *Administración y Comercio*, *A Distancia*) y estandarización para `edad_ingreso`.

### 2.2 Selección de Modelos Logísticos
Se contrastaron tres especificaciones de la probabilidad $\pi_i = P(Y_i = 1 \mid \mathbf{x}_i)$:

| Modelo | Covariables | Parámetros | AIC | BIC | Pseudo $R^2$ |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **$M_1$ (Teórico S1/S2)** | Sexo, Área, Jornada | 15 | 75.745,4 | 75.883,4 | 0,0627 |
| **$M_2$ (S1/S2 + Edad)** | Sexo, Área, Jornada, Edad ingreso | 16 | **75.421,2** | **75.568,5** | **0,0667** |
| **$M_3$ (Stepwise)** | Área, Sexo, Jornada, Edad ingreso | 16 | 75.421,2 | 75.568,5 | 0,0667 |

*Selección:* $M_2$ fue seleccionado unánimemente: minimiza AIC/BIC, coincide con la selección stepwise y posee plena coherencia teórica con los hallazgos de correlación de S1 y S2.

### 2.3 Estabilidad Paramétrica mediante Bootstrap ($B = 1.000$)

| Variable / Nivel | $	ext{OR} = e^{\widehat{eta}}$ | IC 95 % Wald | IC 95 % Bootstrap | Ratio Ancho Boot/Wald | Estabilidad |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Edad de ingreso (año)** | 1,035 | [1,031; 1,039] | [1,016; 1,056] | 5,29 | Robusto |
| **Mujer (vs Hombre)** | 0,749 | [0,721; 0,778] | [0,698; 0,800] | 1,78 | Robusto |
| **Área: Agropecuaria** | 2,419 | [2,190; 2,671] | [1,304; 4,594] | 6,84 | Robusto |
| **Área: Arte y Arquitectura** | 1,191 | [1,080; 1,313] | [0,786; 1,716] | 4,01 | Sensible |
| **Área: Ciencias Básicas** | 2,026 | [1,803; 2,277] | [1,300; 2,995] | 3,58 | Robusto |
| **Área: Ciencias Sociales** | 0,578 | [0,535; 0,623] | [0,401; 0,807] | 4,62 | Robusto |
| **Área: Derecho** | 4,423 | [4,066; 4,811] | [2,854; 6,524] | 4,93 | Robusto |
| **Área: Educación** | 0,700 | [0,647; 0,758] | [0,471; 1,001] | 4,77 | Límite |
| **Área: Humanidades** | 1,160 | [0,962; 1,398] | [0,818; 1,698] | 2,01 | No signif. |
| **Área: Salud** | 0,918 | [0,858; 0,982] | [0,636; 1,242] | 4,90 | Sensible |
| **Área: Tecnología / Ing.** | 2,139 | [2,015; 2,271] | [1,446; 3,051] | 6,26 | Robusto |
| **Jornada: Diurna** | 2,264 | [2,069; 2,478] | [1,038; 4,780] | 9,16 | Robusto |
| **Jornada: Vespertina** | 1,881 | [1,730; 2,045] | [0,998; 3,385] | 7,57 | Límite |
| **Jornada: Semipresencial** | 1,077 | [0,846; 1,372] | [0,565; 1,574] | 1,92 | No signif. |

*Conclusión de Estabilidad:* Las variables estructurales (Mujer, Edad, Derecho, Agropecuaria, Tecnología, Ciencias Básicas) mantienen significancia estricta en el 100 % de las réplicas bootstrap. Sin embargo, los intervalos se ensanchan entre 1,8x y 9,2x producto del agrupamiento de alumnos por universidad, demostrando la necesidad de cautela al interpretar la precisión de Wald.

### 2.4 Diagnóstico de Supuestos y Rendimiento en Test
* $	ext{VIF} < 2,5$ (sin multicolinealidad).
* Linealidad en logit validada por Box-Tidwell y distancias de Cook $< 0,02$.
* **Métricas en Test ($n=31.519$):** $	ext{AUC} = 0,6755$, Exactitud $= 65,87\,\%$, Sensibilidad $= 59,50\,\%$, Especificidad $= 67,87\,\%$ (umbral de Youden $= 0,2246$). Brier Score $= 0,1658$.

---

## 3. Impacto de la Imputación sobre el Modelo Final (Parte 3)

### 3.1 Diseño Experimental de la Prueba Común
Para aislar el efecto de la técnica de imputación, se reajustó la especificación de $M_2$ sobre los tres conjuntos ($E_1, E_2, E_3$) y se evaluó sobre un **subconjunto común de 27.508 titulados con atraso estrictamente observado** (evitando juzgar a los modelos con etiquetas autogeneradas).

### 3.2 Desempeño Comparativo

| Estrategia | AUC | $\Delta	ext{AUC}$ vs $E_1$ [IC 95 %] | Exactitud | Prob. Media Predicha | Prevalencia Real |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **$E_1$ · Eliminación** | 0,6666 | — | 65,55 % | 24,57 % | 24,53 % |
| **$E_2$ · Imputación simple** | 0,6442 | $-0,0224$ [$-0,0273; -0,0187$] | 65,40 % | **28,03 %** | 24,53 % |
| **$E_3$ · Regresión lineal** | 0,6617 | $-0,0049$ [$-0,0066; -0,0032$] | 65,30 % | 24,16 % | 24,53 % |
| **MI · Imputación múltiple** | **0,6640** | $-0,0026$ [$-0,0041; -0,0010$] | 65,50 % | 24,40 % | 24,53 % |

### 3.3 Hallazgos Analíticos y Corrección mediante Imputación Múltiple (MI)
1. **Sexo y Áreas son inmunes a la imputación:** El efecto de género ($	ext{OR} pprox 0,75 - 0,76$), Derecho ($	ext{OR} pprox 4,3$) y Tecnología ($	ext{OR} pprox 2,1$) es idéntico entre estrategias.
2. **Imputación simple descalabrada:** $E_2$ invierte 3 jornadas y sobrestima el riesgo en 3,5 puntos globales (y hasta en 55 puntos en la modalidad a distancia).
3. **Imputación no congeniada en $E_3$:** La regresión de duración inicial omitió *jornada*, asignando una tasa plana de atraso alto ($pprox 20\,\%$) a todas las modalidades. Como A Distancia tenía 75,9 % de incompletos, su tasa cayó artificialmente, disparando el OR de la Diurna a 2,26 y cruzando a Semipresencial por sobre el 1 ($	ext{OR}=1,08$).
4. **Solución MI ($m=20$, congeniada):** Al incluir jornada, sexo y edad en la imputación, los ORs se re-alinean: Diurna baja a 1,60 ($[1,42; 1,80]$) y Semipresencial vuelve a 0,62 ($[0,46; 0,83]$), reduciendo la discrepancia con $E_1$ de 18,5 % a 7,3 %.

---

## 4. Discusión, Conclusiones y Recomendaciones Directivas (Parte 4)

### 4.1 Progresión Metodológica Acumulativa ($S_1 	o S_2 	o S_3$)
* **S1:** Detección de atípicos Tukey sin descarte apresurado; hallazgo de la pérdida administrativa del 12,75 %.
* **S2:** Demostración con Bootstrap BCa de que el área curricular media la brecha de género (de $+1,07$ a $+0,55$ semestres) y cuantificación de la dependencia jerárquica universitaria (Jackknife).
* **S3:** Imputación informada por covariación de S2, clasificación logística supervisada, auditoría del sesgo de no-congenialidad e inferencia robusta bootstrap.

### 4.2 Recomendaciones de Gestión
1. **Sistemas de Alerta Temprana Diferenciados por Área:** Focalizar recursos de tutorías y acompañamiento en Derecho ($	ext{OR}=4,35$), Tecnología e Ingeniería ($	ext{OR}=2,07$) y Ciencias Básicas ($	ext{OR}=2,03$).
2. **Revisión de Plazos de Gratuidad y Financiamiento:** Reconocer que el 24,5 % de atraso severo obedece a factores estructurales del currículo, requiriendo mecanismos de extensión proporcional para evitar el sobreendeudamiento terminal.
3. **Estándares Metodológicos en Analítica de Datos:** Descartar de plano la imputación por la media/mediana en modelos institucionales; exigir imputación múltiple congeniada y ajuste por conglomerados.

---

## 5. Distribución de la Presentación y Repositorio (Parte 5)

### 5.1 Estructura del Video Grupal (10 minutos)
* **Bloque 1 (00:00 - 02:30) · Fernanda Ovalle:** Contexto universitario chileno, calidad de datos S1 y diagnóstico MAR.
* **Bloque 2 (02:30 - 05:00) · Jorge Álvarez:** Inferencia no paramétrica en S2 (Bootstrap BCa, Monte Carlo y Jackknife).
* **Bloque 3 (05:00 - 07:30) · César Lorca:** Construcción y selección del modelo logístico $M_2$ en S3 y curvas ROC.
* **Bloque 4 (07:30 - 10:00) · Sebastián Cajales:** Estabilidad bootstrap por clúster, descubrimiento de no-congenialidad y síntesis directiva $S_1 	o S_2 	o S_3$.

### 5.2 Trazabilidad en GitHub
Código y datos disponibles de manera reproducible en:  
[https://github.com/jaossandon/sumativa1-f2-mcdi501](https://github.com/jaossandon/sumativa1-f2-mcdi501)
