# Impacto de la imputación sobre el modelo final

*Sección para el informe integrado de la Sumativa 3 · Jorge Álvarez Ossandón*

> **Para quien arme el informe.** Son unas 1.700 palabras más tres tablas y
> dos figuras: alrededor de tres páginas de las diez disponibles. Si
> hace falta recortar, el orden pensado es este:
>
> 1. §4 (amplitud de intervalos) se puede reducir a sus dos últimas frases.
> 2. La figura `s3_06` (ROC) se puede quitar: la Tabla 2 dice lo mismo en números.
> 3. En §2, el párrafo sobre E2 cabe en una frase remitiendo a la figura `s3_05`.
>
> Con esos tres recortes queda en unas dos páginas. **Lo que no se puede
> quitar es la Tabla 1 y el párrafo que la explica (§3)**: es la evidencia de
> por qué el conjunto base distorsiona el efecto de la jornada, y sin ella la
> recomendación final no tiene respaldo.
>
> Las figuras están en `S3/informe/figuras/` y todas las tablas en
> `S3/resultados/impacto_*.csv`.

---

## 1. Diseño de la comparación

La sección de preparación eligió la imputación por regresión (E3) como
conjunto base y dejó la elección sujeta a verificación empírica. Esta sección
la hace: reajusta **la misma especificación del modelo final** —el M2 de la
sección de modelamiento: sexo, área de conocimiento, jornada y edad de
ingreso— sobre los tres conjuntos, con las mismas 16 columnas y las mismas
categorías de referencia, y compara coeficientes, amplitud de intervalos y
desempeño. Como control, el M2 reajustado sobre E3 reproduce el de la
sección anterior con diferencias menores a 0,011 en los odds ratios.

La comparación exige dos decisiones de diseño. La primera es **evaluar los
tres modelos sobre los mismos casos y contra la misma verdad**: si cada uno se
evaluara en su propia partición de prueba, E1 lo haría sin los casos más
difíciles y E2 y E3 serían juzgados contra etiquetas que ellos mismos
generaron. Se reconstruyó la partición 70/30 de la sección de preparación y
se tomó como **prueba común** el subconjunto con atraso **observado**: 27.508
titulados, con 24,53 % de atraso alto.

La segunda es la referencia para los coeficientes. La eliminación de casos es
sesgada para medias y proporciones cuando la pérdida es MAR, como se mostró
en la sección anterior, pero **los coeficientes de una regresión estimada con
casos completos son insesgados cuando la pérdida depende de los predictores
del modelo**, y aquí depende principalmente de la jornada, que es uno de
ellos. E1 pierde precisión, no validez. Por eso sirve de referencia.

## 2. Efecto sobre los coeficientes

**Sexo, área y edad de ingreso son robustos a la estrategia.** Entre E1 y E3
los odds ratios de estas variables cambian menos de 9 %, salvo Educación
(−16 %), que conserva el lado del 1. La brecha por sexo —OR de 0,76 para
mujeres en E1 y 0,75 en E3— no depende de cómo se traten los faltantes, lo
que es consistente con la robustez en signo que documentó la S2.

**La imputación simple invierte conclusiones.** E2 da vuelta el signo de
tres de las cuatro jornadas y de Educación (OR de 0,83 a 1,58). La jornada
diurna, que en E1 aumenta las chances de atraso alto frente a la modalidad a
distancia (OR 1,38), aparece como protectora (OR 0,09). El pseudo R² se
duplica (0,145 frente a 0,059), pero no porque el modelo explique mejor: está
explicando un patrón que creó la imputación.

**La imputación por regresión distorsiona la jornada.** El cambio medio
absoluto de E3 frente a E1 es de 18,5 %, y está concentrado en esa variable:
Diurna sube de 1,38 a 2,26 y Semipresencial pasa de 0,51 a 1,08, cambiando de
lado del 1.

*[Figura: `s3_05_or_por_estrategia.png`]*

## 3. Por qué E3 falla en la jornada

La Tabla 1 compara, por jornada, el porcentaje de atraso alto de los casos
observados con el que cada estrategia asigna a los imputados.

**Tabla 1.** Porcentaje de atraso alto: observados frente a lo asignado a los imputados

| Jornada | % imputado | Observados | E2 | E3 | MI |
|---|---:|---:|---:|---:|---:|
| A Distancia | 75,9 | 22,6 | 97,8 | 19,2 | 24,5 |
| Diurna | 1,5 | 23,9 | 29,7 | 19,8 | 22,7 |
| Otra | 51,6 | 22,4 | 79,3 | 17,1 | 11,3 |
| Semipresencial | 54,1 | 10,5 | 99,8 | **21,2** | 15,0 |
| Vespertina | 36,9 | **32,9** | 89,7 | **18,5** | 21,7 |

E2 asigna atraso alto a entre el 80 % y el 100 % de los imputados: la mediana
asigna la misma duración a todos y, como se concentran en carreras cortas, la
resta con la duración formal produce atrasos artificiales.

E3 asigna **entre 17 % y 21 % en todas las jornadas por igual**, mientras que
en los observados la jornada sí diferencia, de 10,5 % en Semipresencial a
32,9 % en Vespertina. La razón es que el modelo de imputación no incluyó la
jornada entre sus predictores. Es lo que la literatura llama una imputación
**no congeniada**: cuando el modelo de imputación omite una variable que el
modelo de análisis sí usa, los imputados pierden la asociación con ella y se
aproximan a un promedio común.

El efecto sobre los odds ratios no es un simple acercamiento al 1, porque la
categoría de referencia, A Distancia, es la más imputada (75,9 %). Al bajar
el atraso de la referencia, la jornada diurna, casi sin imputados, aparece
más riesgosa en comparación. Al subir el de Semipresencial de 10,5 % a cerca
de 16 %, esta se acerca a la referencia y su OR cruza el 1.

## 4. Amplitud de los intervalos

Con intervalos de Wald, el ancho mediano de E3 es 0,927 veces el de E1, casi
exactamente lo que se espera solo por tener más observaciones (√(64.159 /
73.544) = 0,934). El modelo trata los 13.396 valores imputados como si fueran
tan informativos como los observados, cuando son predicciones con un error
típico de 2,3 semestres: es **precisión prestada**. E2 llega a 0,900, más
estrecho de lo que justifica el tamaño.

Esa subestimación, sin embargo, es menor frente a la que produce ignorar la
agrupación por universidad. Con errores estándar agrupados por institución,
los intervalos se ensanchan **4,5 a 5,5 veces** en los tres conjuntos, en
línea con la S2 (3,5 veces) y con el bootstrap por institución de la sección
de modelamiento. La fuente de incertidumbre más subestimada en este problema
es la institucional, no la imputación.

## 5. Desempeño y calibración

**Tabla 2.** Desempeño en la prueba común (27.508 casos con atraso observado)

| Conjunto | AUC | Δ AUC vs E1 [IC 95 %] | Exactitud | Prob. media predicha |
|---|---:|---:|---:|---:|
| E1 · Eliminación | 0,667 | — | 0,656 | 24,6 % |
| E2 · Imputación simple | 0,644 | −0,022 [−0,027; −0,019] | 0,654 | **28,0 %** |
| E3 · Imputación por regresión | 0,662 | −0,005 [−0,007; −0,003] | 0,653 | 24,2 % |
| MI · Imputación múltiple | 0,664 | — | — | 24,4 % |

*Porcentaje real de atraso alto: 24,5 %. IC por bootstrap pareado, B = 500.*

E2 discrimina peor y sobrestima el riesgo en 3,5 puntos. E3 pierde 0,005 de
AUC, una diferencia estadísticamente distinta de cero pero despreciable en
la práctica. **La exactitud no distingue a los tres modelos** (0,653 a 0,656),
porque cada umbral de Youden se ajusta a su modelo. Juzgada solo por esa
métrica, la imputación simple habría parecido inocua.

Dos precisiones. La primera es que el AUC comparable del modelo final es
**0,662** y no el 0,676 reportado en la sección de modelamiento: aquel se
calculó sobre una partición que incluye 4.011 casos cuyas etiquetas fueron
generadas por la propia imputación. La segunda es que **las métricas globales
esconden el daño en los grupos minoritarios**. La jornada diurna representa
el 88 % de la prueba común y en ella los cuatro modelos están calibrados.
Fuera de ella, E2 predice 79,9 % de atraso alto a los titulados a distancia
cuyo atraso real es 24,4 %, y E3 predice 17,4 % en Semipresencial frente a un
8,8 % real. El sesgo crece con el porcentaje imputado de cada jornada.

*[Figura: `s3_06_roc_por_estrategia.png`]*

## 6. Imputación múltiple congeniada

Para comprobar el diagnóstico se repitió la imputación corrigiendo sus dos
limitaciones. El modelo de imputación incorporó todas las variables del M2
(jornada, sexo y edad de ingreso) además de los cuatro predictores
originales, con un ajuste equivalente (R² 0,792, RMSE 2,30). En lugar de un
único valor se generaron **m = 20 imputaciones**, cada una con coeficientes
sorteados de su distribución de muestreo y un residuo extraído de los
residuos empíricos, que preservan la cola pesada de la distribución. El M2 se
ajustó en cada una y los resultados se combinaron con las **reglas de
Rubin**.

**Tabla 3.** Odds ratios bajo cada estrategia

| Variable | E1 | E2 | E3 | MI [IC 95 %] | Fracción de información perdida |
|---|---:|---:|---:|---:|---:|
| Mujer | 0,764 | 0,830 | 0,749 | 0,757 [0,728; 0,787] | 0,06 |
| Edad de ingreso (año) | 1,013 | 1,016 | 1,035 | 1,029 [1,025; 1,034] | 0,36 |
| Diurna | 1,375 | 0,089 | 2,263 | 1,602 [1,421; 1,805] | 0,47 |
| Vespertina | 1,658 | 0,271 | 1,882 | 1,490 [1,325; 1,676] | 0,53 |
| Otra | 1,334 | 0,321 | 1,824 | 1,062 [0,743; 1,517] | 0,38 |
| Semipresencial | 0,513 | 0,495 | 1,077 | 0,618 [0,459; 0,831] | 0,23 |

*Referencia de jornada: A Distancia. IC de MI con varianza total de Rubin.*

La imputación congeniada **corrige la mayor parte de la distorsión**: el
cambio medio frente a E1 baja de 18,5 % a 7,3 %, Semipresencial vuelve a
quedar bajo 1 y Diurna baja de 2,26 a 1,60. Los porcentajes asignados a los
imputados dejan de ser planos (Tabla 1) y la modalidad a distancia queda
calibrada (23,6 % predicho frente a 24,4 % real). Los intervalos son más
anchos que los de E3 en todas las variables —en la jornada pasan de 0,59–0,70
a 0,72–0,95 veces el ancho de E1—, y la fracción de información perdida
cuantifica dónde pesa la imputación: entre 23 % y 53 % en la jornada y 36 %
en la edad de ingreso, frente a menos de 17 % en sexo y áreas.

La corrección no es completa. Diurna queda en 1,60 frente a 1,38 en E1, y a
los imputados de la jornada vespertina se les sigue asignando 21,7 % de
atraso alto frente al 32,9 % observado. Puede reflejar un perfil distinto de
esos titulados o una especificación lineal insuficiente; con los datos
disponibles no es posible distinguirlo. **La dirección del efecto de la
jornada es estable entre E1 y MI; su magnitud es sensible a la imputación en
alrededor de un 20 %.**

## 7. Conclusiones

1. **Las conclusiones sobre sexo, área de conocimiento y edad de ingreso no
   dependen del tratamiento de los faltantes.** La brecha por sexo se
   mantiene en un OR de 0,75 a 0,76 bajo todas las estrategias razonables.
2. **La imputación simple no es admisible**: invierte el efecto de la
   jornada, deteriora la discriminación y sobrestima el riesgo hasta en 55
   puntos en la modalidad a distancia.
3. **El conjunto base E3 es adecuado para predecir, pero no para interpretar
   la jornada.** Su AUC es prácticamente el de E1, pero sus odds ratios de
   jornada están distorsionados porque el modelo de imputación omitió esa
   variable.
4. **Los odds ratios de jornada deben leerse en la versión de imputación
   múltiple** (Tabla 3), con la advertencia de que su magnitud es sensible a
   la imputación y de que en la modalidad a distancia el modelo no
   discrimina (AUC entre 0,50 y 0,55 en todos los conjuntos).
5. **Recomendación metodológica.** El modelo de imputación debe incluir todas
   las variables del modelo de análisis, y los intervalos deben incorporar
   tanto la incertidumbre de la imputación (reglas de Rubin) como la
   agrupación por universidad, que en este problema es la de mayor magnitud.

## 8. Reproducibilidad

El análisis está en `S3/notebooks/S3_03_Impacto_Imputacion.ipynb`, que parte
de los parquet generados por `S3_01_Preparacion_Datos.ipynb`. Los resultados
quedan en `S3/resultados/impacto_*.csv` (ocho archivos) y las figuras en
`S3/informe/figuras/s3_05_or_por_estrategia.png` y
`s3_06_roc_por_estrategia.png`. Semilla 42 en la partición, el bootstrap y
las imputaciones múltiples.
