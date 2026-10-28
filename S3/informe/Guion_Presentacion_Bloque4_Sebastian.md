# Guion de Exposición Oficial: Bloque 4 (Sebastián Cajales)
**Evaluación Sumativa 3: Modelamiento Predictivo Integrado**  
*MCDI501: Estadística Computacional para la Toma de Decisiones — Magíster en Ciencia de Datos e IA, UNAB*  
**Duración asignada:** 2 minutos y 30 segundos (Minuto 07:30 al 10:00 del video grupal)

---

## 1. Estructura y Metas del Bloque 4

Como expositor de cierre del proyecto, este bloque tiene cuatro responsabilidades clave evaluadas en la rúbrica:
1. **Demostrar la robustez computacional del modelo logístico final** mediante Bootstrap por conglomerados ($B = 1.000$), contrastando con los intervalos tradicionales asintóticos de Wald.
2. **Explicar el impacto analítico de la imputación en la toma de decisiones**, revelando el hallazgo de la imputación no congeniada y cómo la Imputación Múltiple ($m=20$) resuelve la distorsión de la jornada.
3. **Resumir la progresión metodológica acumulativa ($S_1 	o S_2 	o S_3$)**, demostrando que ninguna decisión fue aislada.
4. **Formular recomendaciones estratégicas de negocio** para la gestión directiva universitaria y políticas públicas de educación superior.

---

## 2. Diapositivas Asociadas (Presentacion_Bloque4_Sebastian.pptx)

* **Slide 1:** Portada Institucional con Logo UNAB a color, Grupo 6 y título de la presentación.
* **Slide 2:** Estabilidad Bootstrap ($B=1.000$) y Dependencia Institucional (Wald vs. Bootstrap).
* **Slide 3:** Análisis Comparativo de Imputación ($E_1, E_2, E_3, 	ext{MI}$) y Hallazgo de No-Congenialidad.
* **Slide 4:** Progresión Metodológica Acumulativa ($S_1 	o S_2 	o S_3$) y Recomendaciones Directivas.
* **Slide 5:** Repositorio Oficial en GitHub y Cierre de la Presentación.

---

## 3. Guion Palabra por Palabra (Speech con marcas de tiempo)

> *Ritmo recomendado: Pausado, seguro, profesional y con énfasis en los números auditados. Total: ~360 palabras (tiempo estimado: 2 minutos y 20 segundos, con 10 segundos de holgura).*

---

### [07:30 - 08:15] Estabilidad Paramétrica Bootstrap y Agrupamiento Institucional

> *"Muchas gracias, César.*  
> *Para garantizar que las decisiones de gestión no descansen ciegamente en supuestos asintóticos teóricos —que suelen fallar en presencia de asimetría o dependencia jerárquica—, sometimos el modelo logístico final a un remuestreo **bootstrap por conglomerados institucionales con 1.000 réplicas**.*
> 
> *Al contrastar los intervalos asintóticos clásicos de Wald con los empíricos de Bootstrap al 95 %, confirmamos la **alta estabilidad direccional de las variables críticas**: ser mujer tiene un efecto protector significativo con un Odds Ratio de 0,75, mientras que cursar Derecho multiplica las chances de atraso alto por 4,4, y Tecnología por 2,1.*
> 
> *Sin embargo, el hallazgo metodológico clave es que los intervalos bootstrap resultan entre **3,5 y 9,2 veces más anchos** que los de Wald. Esto valida de forma contundente lo que descubrimos en la Sumativa 2 con Jackknife: los estudiantes comparten dinámicas al interior de cada universidad, por lo que ignorar la estructura clúster subestima severamente la verdadera incertidumbre."*

---

### [08:15 - 09:05] Impacto de la Imputación y el Hallazgo de No-Congenialidad

> *"La pregunta central de esta fase era: ¿cambia la decisión del negocio según cómo tratamos el 12,75 % de datos no observados? Evaluamos los modelos sobre una **prueba común de 27.508 titulados con atraso observado**.*
> 
> *Los resultados son categóricos:  
> Primero, **la imputación simple por mediana es inadmisible**: invierte el signo de tres de las cuatro jornadas y sobrestima la prevalencia de atraso alto en más de 3 puntos porcentuales.*  
> 
> *Segundo, al analizar nuestra imputación por regresión, identificamos un fenómeno crucial de la literatura estadística: una **imputación no congeniada**. Al haber omitido la jornada en el modelo lineal de duración, se asignó una tasa plana de atraso a todas las modalidades, distorsionando los Odds Ratios de la jornada diurna y semipresencial.*  
> 
> *Para resolverlo, implementamos una **Imputación Múltiple Congeniada con 20 réplicas y reglas de Rubin**, incorporando jornada, sexo y edad. Con esto, redujimos la distorsión media con casos completos al 7,3 %, recuperamos la calibración en todas las modalidades y alcanzamos un **AUC de 0,662 y una exactitud del 65,3 %**."*

---

### [09:05 - 10:00] Síntesis Acumulativa ($S_1 	o S_2 	o S_3$) y Recomendaciones Directivas

> *"Para cerrar la defensa del Grupo 6, queremos relevar la coherencia de nuestra cadena analítica:*  
> *En **S1**, el análisis exploratorio evitó descartar erróneamente los valores atípicos y detectó la pérdida administrativa.*  
> *En **S2**, los métodos computacionales de remuestreo demostraron que la brecha de género estaba mediada por la carrera y evidenciaron la dependencia institucional.*  
> *Y en esta **S3**, integramos ambos antecedentes para seleccionar covariables con fundamento, auditar la imputación y construir un clasificador reproducible y robusto.*
> 
> *Desde la perspectiva de toma de decisiones y política pública, formulamos dos recomendaciones directivas:*  
> *Primera: implementar **Sistemas de Alerta Temprana focalizados** en facultades de Derecho, Ingeniería y Ciencias Básicas, donde los cuellos de botella de titulación son estructurales y no meramente sociodemográficos.*  
> *Segunda: **flexibilizar los plazos de financiamiento y gratuidad**, dado que el rezago superior a 4 semestres afecta a casi un cuarto del estudiantado universitario chileno.*  
> 
> *Todo el código, notebooks y reportes técnicos se encuentran completamente disponibles en nuestro repositorio oficial de GitHub. Muchas gracias."*

---

## 4. Recomendaciones Finales para el Momento de Grabar

1. **Entonación pausada en los números:** Enfatiza claramente *"1.000 réplicas bootstrap"*, *"Odds Ratio de 0,75"* y *"27.508 titulados en prueba común"*. Son los indicadores que el profesor buscará en la rúbrica de evaluación.
2. **Fluidez en la transición:** Al arrancar con *"Muchas gracias, César"*, demuestras que el video es una pieza orgánica de equipo y no cuatro fragmentos aislados.
3. **Mención explícita a $S_1 	o S_2 	o S_3$:** Es el estándar obligatorio de la Fase 4 para alcanzar el puntaje máximo en comunicación.
