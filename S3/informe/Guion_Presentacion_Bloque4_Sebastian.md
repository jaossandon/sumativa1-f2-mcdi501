# Guion de Exposición: Bloque 4 (Sebastián Cajales)
**Evaluación Sumativa 3: Modelamiento Predictivo Integrado**  
*MCDI501: Estadística Computacional para la Toma de Decisiones — UNAB*  
**Duración asignada:** 2 minutos y 30 segundos (Minuto 7:30 al 10:00 del video grupal)

---

## 1. Resumen y Objetivos del Bloque 4

Como cierre del proyecto, este bloque tiene la responsabilidad de:
1. **Demostrar la robustez computacional del modelo logístico final** mediante Bootstrap ($B \ge 1.000$), contrastando con los intervalos tradicionales asintóticos (Wald).
2. **Presentar el diagnóstico de supuestos:** Multicolinealidad (VIF), linealidad en el logit (Box-Tidwell) y observaciones influyentes.
3. **Responder la pregunta analítica central de la Sumativa 3:** ¿Cambia la decisión del negocio según la estrategia de imputación utilizada?
4. **Cerrar con la progresión metodológica ($S_1 \to S_2 \to S_3$) y recomendaciones estratégicas** para la gestión universitaria y políticas públicas de educación superior.

---

## 2. Diapositivas sugeridas (Qué proyectar en pantalla)

### Diapositiva 1: Estabilidad Bootstrap y Diagnóstico de Supuestos
- **Gráficos:** Distribución empírica bootstrap de los coeficientes / Odds Ratios y curva ROC del modelo final en Test.
- **Puntos clave en pantalla:**
  - $B = 1.000$ réplicas bootstrap no paramétricas.
  - Intervalos percentil y BCa al 95 % vs. intervalos clásicos de Wald.
  - Supuestos verificados: VIF $< 5$ (sin multicolinealidad severa), linealidad logit validada y control de observaciones influyentes (Cook).

### Diapositiva 2: Impacto Analítico de la Imputación en la Toma de Decisiones
- **Tabla resumen:** Comparativa de los 3 datasets (Eliminación listwise $n=91.667$, Imputación simple $n=105.063$, Imputación por regresión $n=105.063$).
- **Métricas:** Variación de coeficientes $\beta$, amplitud de intervalos de confianza, Accuracy y AUC en Test.
- **Veredicto:** ¿Se alteran los factores de riesgo o las conclusiones del negocio?

### Diapositiva 3: Conclusiones Integradas ($S_1 \to S_2 \to S_3$) y Recomendaciones
- **Línea de progresión del proyecto:**
  - $S_1$: Diagnóstico exploratorio y alerta de faltantes del 12,75 %.
  - $S_2$: Validación con remuestreo (Bootstrap, Monte Carlo, Jackknife por universidad).
  - $S_3$: Imputación informada, clasificación predictiva y estabilidad de inferencia.
- **Recomendaciones clave:**
  - Sistema de alerta temprana diferenciado por área curricular y jornada vespertina.
  - Flexibilización de plazos en políticas de gratuidad y financiamiento institucional.

---

## 3. Guion Palabra por Palabra (Speech con marcas de tiempo)

> *Ritmo recomendado: Pausado, seguro y técnico. Total aproximado: ~330 palabras (2 minutos y 15 segundos de habla efectiva, dejando margen de 15 segundos para transición).*

---

### [00:00 - 00:45] Estabilidad Bootstrap y Diagnóstico de Supuestos

> *"Muchas gracias, César.*  
> *Para garantizar que nuestro modelo logístico final no dependa exclusivamente de supuestos asintóticos teóricos que suelen fallar en muestras con agrupamiento o asimetría —como detectamos en la Sumativa 2 mediante Jackknife—, aplicamos un remuestreo **bootstrap no paramétrico con 1.000 réplicas** sobre el conjunto de entrenamiento.*
> 
> *Al contrastar los intervalos asintóticos tradicionales de Wald con los intervalos bootstrap percentil y BCa al 95 %, confirmamos una **alta estabilidad paramétrica**: los coeficientes de las variables de mayor impacto —como la jornada vespertina, la edad de titulación y las áreas tecnológicas— mantienen intervalos estrechos y sin cruzar el valor nulo de Odds Ratio igual a 1.*
> 
> *Asimismo, el diagnóstico de supuestos ratificó la validez del modelo: los Factores de Inflación de Varianza se ubicaron bajo el umbral de 5 descartando multicolinealidad, la linealidad en el logit fue consistente según Box-Tidwell y no se identificaron puntos de apalancamiento que distorsionaran sustantivamente las probabilidades estimadas."*

---

### [00:45 - 01:30] Análisis Comparativo del Impacto de la Imputación

> *"Uno de los focos evaluativos más relevantes de esta Sumativa 3 fue evaluar si la estrategia para tratar el 12,75 % de datos no observados altera o no las decisiones institucionales.*  
> *Para responder a esto, re-ajustamos la especificación del modelo final sobre los tres escenarios:*
> 1. *Eliminación de casos completos (perdiendo más de 13.000 observaciones).*
> 2. *Imputación simple por mediana.*
> 3. *Nuestra imputación por regresión lineal múltiple.*
> 
> *Los resultados son categóricos: aunque la eliminación de casos completos preserva la dirección general de los efectos, **la imputación por regresión maximiza la potencia estadística sin inflar artificialmente la precisión**, logrando un desempeño predictivo sólido en el conjunto de prueba `[mencionar AUC final de 0.XX y Accuracy de XX %]`, demostrando que los factores de riesgo identificados son estructurales y no un artefacto de la falta de datos."*

---

### [01:30 - 02:30] Conclusiones Integradas ($S_1 \to S_2 \to S_3$) y Recomendaciones

> *"Para concluir la exposición grupal, queremos destacar la progresión metodológica integral de este proyecto:*
> - *En **S1**, el análisis exploratorio evitó descartar erróneamente los valores atípicos y caracterizó la asimetría del rezago.*
> - *En **S2**, los métodos computacionales de remuestreo demostraron que la brecha de género se explicaba por el área de estudio y que existía una fuerte dependencia institucional.*
> - *Y en esta **S3**, integramos ambos antecedentes para imputar con fundamento teórico y construir un clasificador logístico robusto y validado computacionalmente.*
> 
> *En términos de negocio y política educativa, nuestras dos recomendaciones clave son:*
> *Primero, diseñar **Sistemas de Alerta Temprana focalizados**, donde las tutorías y el seguimiento académico se concentren de manera prioritaria en facultades de Ingeniería y Tecnología, con especial flexibilidad para los estudiantes de jornada vespertina.*
> *Y segundo, **revisar los plazos rígidos de financiamiento y gratuidad**, considerando que el atraso superior a 4 semestres no es una anomalía individual aislada, sino un fenómeno estructural del sistema formativo universitario chileno.*
> 
> *Muchas gracias por su atención y quedamos atentos a sus preguntas."*

---

## 4. Tips Clave para el Momento de Grabar

1. **Entonación en los números:** Cuando menciones "1.000 réplicas bootstrap" o "12,75 % de faltantes", dilo con claridad y énfasis, ya que son los requisitos explícitos de la pauta.
2. **Conexión con el compañero previo:** Empezar con *"Gracias, César"* le demuestra al profesor que el grupo está coordinado y no son 4 presentaciones pegadas al azar.
3. **Mención explícita a $S_1 \to S_2 \to S_3$:** Es el criterio que más puntos entrega en el ítem de comunicación según la rúbrica.
