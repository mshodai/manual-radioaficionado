# Escucha y bandas de uso libre

Antes de transmitir, cualquier radioaficionado ha pasado horas escuchando. En este capítulo aprenderás qué es la escucha de radio, qué se puede oír con un receptor sencillo o desde un navegador, cómo se pide una tarjeta QSL de escucha y qué dice la ley española sobre escuchar y contar lo que oyes. Después verás las bandas que puedes usar **sin ninguna autorización**: PMR446, la banda ciudadana CB-27 y los dispositivos de corto alcance de 433 y 868 MHz, con sus límites exactos. Te servirá para empezar en la radio antes del examen y para no confundir lo que permite cada régimen: lo que es legal en la banda ciudadana no lo es en PMR446, y al revés.

## La escucha

### Qué es

Un **escucha** (en inglés, *shortwave listener*, de donde viene la sigla **SWL**) es quien sigue las emisiones de radio sin transmitir. No necesita autorización ni examen: basta un receptor y una antena. Muchos radioaficionados empezaron así, y la escucha sigue siendo la mejor escuela. Aprendes cómo suena cada modo, cómo se hace un contacto, a qué hora se abre cada banda y cómo afecta el ciclo solar que viste en el [capítulo 5](05-propagacion-bandas.md#el-ciclo-solar).

### El receptor

Cualquier receptor sirve para empezar, pero conviene que tenga tres cosas:

- **Cobertura de onda corta**, de 3 a 30 MHz como mínimo, con sintonía fina.
- **Banda lateral única** (BLU, *SSB*), sin la que no entenderás la fonía de los radioaficionados en HF ni las señales digitales. Un receptor que solo tiene AM y FM se queda en la radiodifusión.
- **Toma de antena exterior**. La antena telescópica funciona, pero unos metros de hilo fuera de casa multiplican lo que oyes.

Los tipos de receptor, sus etapas y lo que significan la sensibilidad y la selectividad se tratan en el [capítulo 7](07-equipos.md#receptores), con el ejemplo de un receptor portátil multibanda con BLU. Las antenas de hilo y la forma de alejarlas del ruido de la casa, en el [capítulo 6](06-antenas-lineas.md#antenas-de-hilo-no-resonantes).

Un **receptor SDR** (*software defined radio*) de bajo coste conectado a un ordenador es otra opción muy extendida: digitaliza una porción ancha del espectro y el programa la presenta como una **cascada**, en la que ves de un vistazo todas las señales de la banda.

### Receptores SDR en la web

No necesitas tener receptor para empezar. Hay receptores SDR instalados por aficionados de todo el mundo que puedes sintonizar desde el navegador, cada uno con su antena y su ubicación:

- **WebSDR.** Según [websdr.org](http://websdr.org/), es un receptor SDR conectado a Internet que permite a muchos oyentes escucharlo **a la vez y sintonizar cada uno por su cuenta**, a diferencia de los receptores clásicos accesibles por Internet. El programa es obra de PA3FWM, que mantiene esa página con la lista de servidores activos, filtrable por banda y por región (comprobado en noviembre de 2026).
- **KiwiSDR.** Es un receptor de red que, según el [documento de diseño](http://kiwisdr.com/docs/KiwiSDR/KiwiSDR.design.review.pdf) que publica su web, cubre de **10 kHz a 30 MHz**, de la onda muy larga a la onda corta. La [web de KiwiSDR](http://kiwisdr.com/) enlaza la lista y el mapa de receptores públicos en [kiwisdr.com/public](http://kiwisdr.com/public/) y una función de radiogoniometría colectiva, **TDoA**, que estima de dónde viene una señal comparando cuándo llega a varios receptores (comprobado en noviembre de 2026).

Los receptores web son perfectos para comprobar si tu propia señal llega lejos: llamas, y te escuchas en un receptor a mil kilómetros. También sirven para comparar la propagación desde distintos puntos, o para escuchar en HF si vives en un piso sin sitio para una antena.

!!! example "En la práctica"
    Cuando uses un receptor web para oírte a ti mismo, ten en cuenta el retardo: entre que hablas y te oyes pasan uno o varios segundos. Y deja el receptor libre cuando acabes: cada uno admite un número limitado de oyentes a la vez.

### Qué se puede escuchar

**Radiodifusión en onda corta.** Las emisoras internacionales emiten en bandas atribuidas al servicio de radiodifusión que se conocen por su longitud de onda aproximada. En la columna de atribución nacional del [Cuadro Nacional de Atribución de Frecuencias](https://www.boe.es/buscar/act.php?id=BOE-A-2026-15661) (CNAF), aprobado por la Orden TDF/732/2026, de 10 de julio, figuran, entre otras, estas (páginas 101103 a 101109 del BOE; comprobado en noviembre de 2026):

| Banda | Márgenes en el CNAF |
|---|---|
| 49 m | 5900 – 6200 kHz |
| 41 m | 7200 – 7450 kHz |
| 31 m | 9400 – 9900 kHz |
| 25 m | 11 650 – 12 050 kHz |
| 19 m | 15 100 – 15 600 kHz |

Comprueba la relación con la fórmula del [capítulo 4](04-teoria-radio.md): en 9650 kHz, $\lambda = 300 / 9{,}65 \approx 31\ \text{m}$. Las bandas bajas (49 y 41 m) se oyen mejor de noche y las altas (25 y 19 m), de día, por lo que viste en el [capítulo 5](05-propagacion-bandas.md#variaciones-diarias-y-estacionales). La de 41 m empieza justo donde acaba la de aficionados de 40 m: de noche oirás emisoras potentes pegadas al borde superior de la banda.

**Radioaficionados.** Fonía en BLU, telegrafía, modos digitales, satélites y repetidores. Es lo que más te enseña para el examen y para tu futura estación. Escucha cómo se estructura un contacto ([capítulo 10](10-operacion.md)), descodifica FT8 con el ordenador ([capítulo 12](12-modos-digitales.md)) o sigue un concurso un fin de semana: en pocas horas oirás decenas de países.

**Balizas.** Las radiobalizas de aficionado emiten de forma continua desde un punto conocido. Si oyes la baliza, la banda está abierta hacia ese lugar. Las del International Beacon Project y los segmentos de balizas del plan de la IARU los tienes en el [capítulo 5](05-propagacion-bandas.md#balizas-y-seguimiento-de-la-propagacion).

### El cuaderno de escucha

Anota cada escucha: fecha y hora en UTC, frecuencia, modo, estación oída, calidad de la señal y, si los hay, los datos que dio (lugar, programa, estación con la que hablaba). Usa el informe RS que viste en el [capítulo 10](10-operacion.md#el-informe-de-senal-rs-y-rst) para valorar la señal. Con el tiempo, ese cuaderno te dirá qué bandas se abren a qué hora desde tu casa mejor que cualquier predicción.

### La tarjeta QSL de escucha

Una **tarjeta QSL de escucha** (*SWL card*) es la que envía un escucha a una estación para confirmar que la ha oído. La estación, si quiere, contesta con su propia QSL. Para que el informe tenga valor, tiene que demostrar que de verdad oíste la emisión:

- **A un radioaficionado**: fecha, hora UTC, banda, frecuencia y modo; el indicativo de la estación con la que hablaba y algún detalle del contacto; tu informe RS o RST, y tu equipo y antena. Indica claramente que es un informe de escucha («SWL report»), no un contacto.
- **A una emisora de radiodifusión**: varios minutos de programación con detalles comprobables (títulos, temas, la hora de cada cosa), la frecuencia, la calidad de la señal y las interferencias. Muchas emisoras aceptan informes por correo electrónico y contestan con una QSL de recepción.

Puedes enviarlas por las mismas vías que viste en el [capítulo 10](10-operacion.md#las-tres-vias): directa por correo, por bureau si una asociación te da ese servicio, o por un sistema electrónico que admita escuchas.

!!! example "En la práctica"
    Ejemplo de datos para una QSL de escucha a una estación ficticia: «EA0ZZZ oída el 14-3 a las 19:42 UTC en 7155 kHz, LSB, en contacto con EA0YYY. RS 57, desvanecimiento lento. Receptor portátil con BLU y 10 m de hilo». Con eso la estación lo comprueba en su libro de guardia en un minuto.

### Lo que dice la ley sobre escuchar

Escuchar no requiere ninguna autorización, pero no todo lo que se oye se puede escuchar ni contar. Lo regulan dos normas:

**La [Ley 11/2022, de 28 de junio, General de Telecomunicaciones](https://www.boe.es/buscar/act.php?id=BOE-A-2022-10757).** El artículo 106.15 de la Ley 11/2022 tipifica como **infracción muy grave** «la interceptación, sin autorización, de telecomunicaciones no destinadas al público en general, así como la divulgación del contenido» (comprobado en noviembre de 2026). El artículo 109.1.a) de la Ley 11/2022 castiga las infracciones muy graves con multa de hasta **veinte millones de euros** (comprobado en noviembre de 2026). Fíjate en que la ley sanciona dos conductas distintas: interceptar y divulgar.

**El [Código Penal](https://www.boe.es/buscar/act.php?id=BOE-A-1995-25444#a197).** El artículo 197.1 del Código Penal castiga con prisión de uno a cuatro años a quien, **para descubrir los secretos o vulnerar la intimidad de otro** y sin su consentimiento, intercepte sus telecomunicaciones o use artificios técnicos de escucha. El artículo 197.3 del Código Penal agrava la pena, de dos a cinco años, si se difunden o revelan los hechos descubiertos (comprobado en noviembre de 2026).

La Ley 11/2022 no define qué telecomunicaciones están «destinadas al público en general». Lo que sí está claro:

- **La radiodifusión** está destinada al público por definición: el CNAF define el servicio de radiodifusión como aquel «cuyas emisiones se destinan a ser recibidas directamente por el público en general» (comprobado en noviembre de 2026).
- **Las bandas de aficionado** son abiertas: el artículo 30.2 de la [Orden IET/1311/2013](https://www.boe.es/buscar/act.php?id=BOE-A-2013-7624#a30) prohíbe codificar las transmisiones entre estaciones de aficionado para ocultar su significado (comprobado en noviembre de 2026). Escucharlas es la base de la radioafición y de la preparación del examen.
- **El resto** (servicios profesionales, de seguridad, de empresas, telefonía) no está destinado al público. Que tu receptor sintonice esas frecuencias no significa que puedas escucharlas, y en ningún caso puedes grabar, publicar o contar a otros lo que digan.

!!! danger "Peligro"
    No publiques en redes sociales grabaciones ni transcripciones de comunicaciones que no sean de radiodifusión o de radioaficionados, aunque las hayas captado por casualidad. Divulgar el contenido es una infracción muy grave por sí misma, con independencia de cómo lo captaras. Y si lo que captas es una llamada de socorro, avisa al **112**.

## PMR446

### Qué es

**PMR446** son los *walkie-talkies* de uso libre que se venden en cualquier tienda: portátiles de mano, de poca potencia y con antena fija. La nota UN-110 del CNAF los define como un sistema de radio de corto alcance que opera en la banda de **446,0 a 446,2 MHz** con la consideración de **uso común** (página 101259 del BOE; comprobado en noviembre de 2026). Uso común significa, según el artículo 19.1 del [Real Decreto 123/2017, de 24 de febrero, por el que se aprueba el Reglamento sobre el uso del dominio público radioeléctrico](https://www.boe.es/buscar/act.php?id=BOE-A-2017-2460), que se usa **sin ningún título habilitante**, sin límite de usuarios y con las condiciones técnicas del CNAF (comprobado en noviembre de 2026). Ni licencia, ni registro, ni tasa.

La norma europea es la [Decisión ECC/DEC/(15)05 de la CEPT](https://docdb.cept.org/document/448), de 3 de julio de 2015 y modificada el 2 de marzo de 2018, que la nota UN-110 cita expresamente. Obliga a los países de la CEPT a eximir estos equipos de licencia individual y a permitir su libre circulación y uso (comprobado en noviembre de 2026). Por eso tu PMR446 vale igual en Francia o en Alemania.

### Canales

La nota UN-110 del CNAF fija la canalización y la primera portadora; el número de canales sale de dividir los 200 kHz de la banda entre la separación de canales (comprobado en noviembre de 2026):

| Modo | Separación | Primera portadora | Canales en 200 kHz |
|---|---|---|---|
| Analógico (FM) | 12,5 kHz | 446,00625 MHz | 16 |
| Digital | 6,25 kHz | 446,003125 MHz | 32 |
| Digital | 12,5 kHz | 446,00625 MHz | 16 |

La frecuencia del canal analógico $n$ es

$$
f_n\,(\text{MHz}) = 446{,}00625 + (n - 1) \cdot 0{,}0125
$$

donde $n$ va de 1 a 16 y 0,0125 MHz son los 12,5 kHz de separación.

**Ejemplo.** El canal 8 está en $446{,}00625 + 7 \cdot 0{,}0125 = 446{,}09375\ \text{MHz}$, y el 16, el último, en $446{,}00625 + 15 \cdot 0{,}0125 = 446{,}19375\ \text{MHz}$, a 6,25 kHz del borde de la banda, la mitad de un canal.

Los equipos analógicos suelen añadir **subtonos** CTCSS o códigos DCS ([capítulo 10](10-operacion.md#tonos-de-acceso-ctcss-y-1750-hz)), que muchos fabricantes llaman «códigos de privacidad». No son privados: solo silencian el altavoz mientras no llega el tono elegido, como viste con los repetidores en el [capítulo 10](10-operacion.md#tonos-de-acceso-ctcss-y-1750-hz). Cualquiera en el mismo canal te oye.

### Modos digitales

La ECC/DEC/(15)05 cita dos especificaciones de ETSI para el PMR446 digital: la TS 102 490 para los equipos de **6,25 kHz**, que es el **dPMR446**, y la TS 102 361-1 para los de **12,5 kHz**, que es el **DMR** en su versión sin repetidores (comprobado en noviembre de 2026). El DMR lo viste en el [capítulo 12](12-modos-digitales.md). Un equipo digital y uno analógico no se entienden entre sí, ni un dPMR con un DMR. Desde el 1 de enero de 2018, la decisión permite el PMR446 digital en toda la banda de 446,0 a 446,2 MHz; hasta entonces estaba limitado a la mitad superior (comprobado en noviembre de 2026).

### Potencia y antena

Según la nota UN-110 del CNAF (comprobado en noviembre de 2026):

- Potencia máxima de **500 mW p. r. a.** (potencia radiada aparente, referida a un dipolo de media onda).
- **Antena incorporada**: equipos portátiles, sin posibilidad de cambiar la antena.
- Funcionamiento **símplex**, transmitiendo y recibiendo en el mismo canal.
- **No** pueden usarse como estación base ni como repetidor, ni conectarse a otras redes o infraestructuras.
- Los equipos cumplen los requisitos de la Directiva 2014/53/UE con la norma armonizada **ETSI EN 303 405**.

La ECC/DEC/(15)05 añade que todo equipo PMR446 tiene que poder recibir, y que los que tienen un PTT que se puede dejar enclavado, o no tienen PTT y transmiten por VOX, cortan la emisión a los **180 segundos** como máximo (comprobado en noviembre de 2026). Así un equipo olvidado con el PTT pulsado no bloquea un canal para siempre.

!!! tip "Para el examen"
    Un transceptor de radioaficionado que cubre 446 MHz **no** es un PMR446, aunque lo sintonices en la misma frecuencia. Tiene antena desmontable, más de 500 mW y no está certificado con la norma EN 303 405, así que transmitir con él en la banda de PMR446 incumple la nota UN-110 del CNAF, tengas o no autorización de radioaficionado. Y al revés: con un PMR446 no puedes transmitir en las bandas de aficionado.

## La banda ciudadana CB-27

### Qué es y qué norma la regula

La **banda ciudadana** (en inglés, *Citizens' Band*, **CB**) ocupa de **26 960 a 27 410 kHz**, en la parte alta de la HF, justo por debajo de la banda de 10 m de aficionados. La regula la nota UN-3 del CNAF (páginas 101224 y 101225 del BOE; comprobado en noviembre de 2026), que la destina exclusivamente a comunicaciones relacionadas con actividades educativas, culturales, deportivas, de ocio o entretenimiento, u otras, **sin ánimo de lucro ni contenido económico**, y le da la consideración de **uso común**.

**Hoy no necesita autorización.** Hasta 2015 había un reglamento propio, aprobado por la Orden ITC/4096/2006, de 28 de diciembre, que exigía autorización. La [Orden IET/614/2015, de 6 de abril](https://www.boe.es/buscar/doc.php?id=BOE-A-2015-3864), lo derogó en el apartado 1 de la disposición derogatoria única de la Orden IET/614/2015 y modificó la nota UN-3 para pasar la CB-27 a uso común. Entró en vigor el 11 de abril de 2015 (comprobado en noviembre de 2026). Si encuentras en un libro o en un foro que hace falta licencia de CB, es información anterior a esa fecha.

La norma europea es la [Decisión ECC/DEC/(11)03 de la CEPT](https://docdb.cept.org/download/1540), de 24 de junio de 2011 y modificada el 17 de junio de 2016, que también exime a los equipos de CB de licencia individual (comprobado en noviembre de 2026).

### Canales

La nota UN-3 del CNAF da **40 canales** con una separación de 10 kHz entre canales adyacentes (comprobado en noviembre de 2026). La numeración no sigue la frecuencia de forma regular: hay saltos y un cruce. Faltan las frecuencias de 26 995, 27 045, 27 095, 27 145 y 27 195 kHz, que la ECC/DEC/(11)03 excluye de la CB (comprobado en noviembre de 2026), y el canal 23 está por encima del 24 y del 25:

| Canal | kHz | Canal | kHz | Canal | kHz | Canal | kHz |
|---|---|---|---|---|---|---|---|
| 1 | 26 965 | 11 | 27 085 | 21 | 27 215 | 31 | 27 315 |
| 2 | 26 975 | 12 | 27 105 | 22 | 27 225 | 32 | 27 325 |
| 3 | 26 985 | 13 | 27 115 | 23 | 27 255 | 33 | 27 335 |
| 4 | 27 005 | 14 | 27 125 | 24 | 27 235 | 34 | 27 345 |
| 5 | 27 015 | 15 | 27 135 | 25 | 27 245 | 35 | 27 355 |
| 6 | 27 025 | 16 | 27 155 | 26 | 27 265 | 36 | 27 365 |
| 7 | 27 035 | 17 | 27 165 | 27 | 27 275 | 37 | 27 375 |
| 8 | 27 055 | 18 | 27 175 | 28 | 27 285 | 38 | 27 385 |
| 9 | 27 065 | 19 | 27 185 | 29 | 27 295 | 39 | 27 395 |
| 10 | 27 075 | 20 | 27 205 | 30 | 27 305 | 40 | 27 405 |

El **canal 9** (27 065 kHz) está reservado al tráfico de **socorro y urgencia** en todo el territorio nacional, y en una emergencia hay que dejarlo libre (nota UN-3; comprobado en noviembre de 2026).

### Modos y potencias

La nota UN-3 del CNAF autoriza estas clases de emisión, todas de telefonía (comprobado en noviembre de 2026):

| Clase | Modulación | Potencia máxima de salida |
|---|---|---|
| 6K00F3E | FM | 4 W |
| 6K00A3E | AM, doble banda lateral | 4 W |
| 3K00H3E | BLU con portadora completa | 12 W p. c. e. |
| 3K00R3E | BLU con portadora reducida | 12 W p. c. e. |
| 3K00J3E | BLU con portadora suprimida | 12 W p. c. e. |

Con carácter experimental admite también modulaciones digitales cuyas emisiones no deseadas no superen las de esas clases, con 4 W como máximo. La designación de las emisiones (6K00 es una anchura de banda de 6 kHz; F3E, telefonía en FM) la viste en el [capítulo 4](04-teoria-radio.md).

??? note "Para saber más"
    La nota UN-3 del CNAF limita la **potencia de salida** del equipo. La ECC/DEC/(11)03, en cambio, limita la **potencia radiada** de la estación, con las mismas cifras: 4 W en modulación angular (FM), 4 W eficaces en doble banda lateral (AM) y 12 W de cresta de la envolvente en BLU (comprobado en noviembre de 2026). No es lo mismo, porque la potencia radiada incluye la ganancia de la antena:

    $$
    P_\text{rad} = P_\text{salida} \cdot 10^{G/10}
    $$

    con $P_\text{rad}$ y $P_\text{salida}$ en vatios y $G$, la ganancia de la antena en decibelios, sin contar las pérdidas del cable. Si los 6 dB que permite la nota UN-3 se miden respecto a un dipolo, una estación de FM con 4 W de salida y esa antena radia $4 \cdot 10^{0{,}6} \approx 16\ \text{W}$ p. r. a. Con el límite de la decisión, la misma antena obligaría a bajar la salida a $4 / 10^{0{,}6} \approx 1\ \text{W}$. En España rige el texto del CNAF: 4 W a la salida del equipo y una antena de 6 dB como máximo. La nota UN-3 no dice si esos 6 dB son respecto a un dipolo o a la antena isótropa: 6 dBi equivalen a $6 - 2{,}15 = 3{,}85$ dBd, una antena algo menos directiva. Si viajas con el equipo a otro país de la CEPT, comprueba cómo ha recogido allí la decisión.

El resto de condiciones de la nota UN-3 (comprobado en noviembre de 2026):

- Está prohibido acoplar **amplificadores** o cualquier dispositivo que dé más potencia de la indicada.
- Funcionamiento **símplex**.
- Antenas de **6 dB de ganancia como máximo** y **sin directividad** en el plano horizontal. Nada de directivas giratorias.
- Prohibidas las estaciones a bordo de **aeronaves**, los **repetidores**, las comunicaciones **por satélite** y la emisión continua de una **portadora sin modular**.
- Los equipos cumplen el Real Decreto 188/2016 y la norma armonizada **ETSI EN 300 433**.
- Los usuarios colaboran con sus medios en las emergencias si la autoridad lo pide, y quien capte una llamada de socorro debe hacerla llegar a la autoridad competente.
- Los canales 1 a 28 se comparten con aplicaciones industriales, científicas y médicas (ICM), que pueden causar interferencias.

!!! example "En la práctica"
    A diferencia del PMR446, en CB puedes montar una estación fija en casa o en el coche con antena exterior, siempre que no pase de 6 dB de ganancia ni sea directiva. Y al estar en 27 MHz, cuando el ciclo solar está alto, la propagación por la ionosfera o por esporádica E lleva tu señal de 4 W a miles de kilómetros, igual que en la banda de 10 m.

## Otras bandas de uso común

El CNAF reserva más bandas de uso común para **dispositivos de corto alcance** (*short range devices*, **SRD**): mandos de garaje, sensores, alarmas, telemetría. La armonización europea está en la [Decisión 2006/771/CE de la Comisión](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32006D0771), cuyo anexo sustituyó la [Decisión de Ejecución (UE) 2025/105](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32025D0105) (comprobado en noviembre de 2026). A diferencia de PMR446 y CB, no son bandas pensadas para conversar, sino para dispositivos que transmiten poco y con poca potencia.

### 433 MHz

La nota UN-30 del CNAF permite, en uso común, dispositivos de corto alcance no específicos en la banda ICM de **433,050 a 434,790 MHz** (página 101231 del BOE; comprobado en noviembre de 2026):

| Banda | Potencia máxima | Condición |
|---|---|---|
| 433,050 – 434,790 MHz | 1 mW p. r. a. | Sin canalización definida |
| 433,050 – 434,790 MHz | 10 mW p. r. a. | Ciclo de trabajo ≤ 10 % |
| 434,040 – 434,790 MHz | 10 mW p. r. a. | Canales de 25 kHz; ciclo de trabajo hasta el 100 % |

Los dispositivos tienen que aceptar las interferencias de las aplicaciones ICM y de otros usos de la banda. Además, la banda de 433,05 a 434,79 MHz está dentro de la de 70 cm de aficionados, de 430 a 440 MHz ([capítulo 5](05-propagacion-bandas.md#tabla-de-bandas)): los radioaficionados también la usan, con mucha más potencia.

En las tiendas se venden *walkie-talkies* para esta banda con el nombre de **LPD** (*low power device*). Ni el CNAF ni la Decisión 2025/105 excluyen la voz en esta banda: lo que limitan es la potencia, **10 mW**, cincuenta veces menos que un PMR446, y el ciclo de trabajo (comprobado en noviembre de 2026). Un equipo que emite con más potencia en 433 MHz no es un LPD legal. Con 10 mW, el alcance práctico es de unos cientos de metros.

### 868 MHz y LoRa

La nota UN-39 del CNAF destina la banda de **868 a 870 MHz** a aplicaciones de baja potencia y datos en uso común (páginas 101233 y 101234 del BOE; comprobado en noviembre de 2026). Para los dispositivos no específicos fija estas subbandas:

| Subbanda | Potencia máxima | Ciclo de trabajo si no usa técnicas de acceso |
|---|---|---|
| 868,000 – 868,600 MHz | 25 mW p. r. a. | 1 % |
| 868,700 – 869,200 MHz | 25 mW p. r. a. | 0,1 % |
| 869,400 – 869,650 MHz | 500 mW p. r. a. | 10 % |
| 869,700 – 870,000 MHz | 5 mW p. r. a. | Sin límite |
| 869,700 – 870,000 MHz | 25 mW p. r. a. | 1 % |

Los huecos entre subbandas son para alarmas fiables y de teleasistencia, con sus propias condiciones. La norma técnica de referencia es la **ETSI EN 300 220**.

El **ciclo de trabajo** es la fracción de tiempo que un dispositivo transmite. La Decisión 2025/105 lo define sobre un periodo de observación de una hora, salvo que se diga otra cosa (comprobado en noviembre de 2026). Los límites solo se aplican si el equipo no usa técnicas de acceso al medio y de mitigación de interferencias equivalentes a las de las normas armonizadas, como escuchar antes de transmitir.

**Ejemplo.** En la subbanda de 869,400 a 869,650 MHz, un 10 % de una hora son $0{,}10 \cdot 3600 = 360\ \text{s}$: seis minutos de emisión por hora como máximo. En la de 868,000 a 868,600 MHz, el 1 % deja solo $0{,}01 \cdot 3600 = 36\ \text{s}$ por hora.

**LoRa** es una modulación de espectro ensanchado muy usada en esta banda para enviar pocos datos a varios kilómetros con muy poca potencia. Sobre ella funciona **Meshtastic**, una red en malla de mensajería que no es radioafición: la verás en el [capítulo 15](15-emergencias/meshtastic.md).

## Comparación

| | Radioaficionado | PMR446 | CB-27 |
|---|---|---|---|
| **Título** | Autorización individual tras examen ([capítulo 1](01-autorizacion.md)) | Ninguno, uso común | Ninguno, uso común (desde abril de 2015) |
| **Frecuencias** | Bandas de aficionado del CNAF, de 135,7 kHz a más de 24 GHz | 446,0 – 446,2 MHz | 26 960 – 27 410 kHz, 40 canales |
| **Potencia máxima** | Según la banda: 1000 W p. c. e. en la mayoría de la HF, 600 W en 2 m, 300 W en 70 cm | 500 mW p. r. a. | 4 W en FM y AM; 12 W p. c. e. en BLU |
| **Antena** | Libre, dentro de las normas de instalación | Incorporada, no se puede cambiar | Exterior permitida, ≤ 6 dB y no directiva |
| **Estaciones** | Fijas, móviles, portátiles, portables, repetidores, satélites | Solo portátiles de mano | Fijas, móviles y portátiles; sin repetidores |
| **Alcance típico** | Local o mundial, según la banda y la propagación | De unos cientos de metros en ciudad a pocos kilómetros en campo abierto | De pocos kilómetros a decenas por onda directa; miles con propagación ionosférica |
| **Usos** | Instrucción, intercomunicación y estudios técnicos, sin fines de lucro | Comunicación entre grupos cercanos: excursiones, obras, eventos | Ocio, deporte y cultura sin contenido económico; carretera; DX con buena propagación |

Las potencias de radioaficionado son las del apartado 3.1 del anexo I de la [Orden IET/1311/2013](https://www.boe.es/buscar/act.php?id=BOE-A-2013-7624#ani), que tienes completas en el [capítulo 5](05-propagacion-bandas.md#tabla-de-bandas); las de PMR446 y CB, las de las notas UN-110 y UN-3 del CNAF (comprobado en noviembre de 2026). Los alcances son orientativos: dependen sobre todo de la altura de las antenas y del terreno, como viste con el horizonte radioeléctrico en el [capítulo 5](05-propagacion-bandas.md#vision-directa-y-horizonte-radioelectrico).

## Resumen

- La **escucha** (SWL) no necesita autorización. Un receptor con onda corta, **BLU** y toma de antena exterior basta para empezar. Los receptores **WebSDR** y **KiwiSDR** se sintonizan desde el navegador.
- Se puede escuchar la **radiodifusión** (49, 41, 31, 25 y 19 m, entre otras), a los **radioaficionados** y las **balizas**. La **QSL de escucha** debe dar datos que la estación pueda comprobar.
- La Ley 11/2022 castiga como **infracción muy grave** la interceptación sin autorización de comunicaciones **no destinadas al público** y la **divulgación** de su contenido (art. 106.15); el Código Penal castiga interceptar para descubrir secretos (art. 197) (comprobado en noviembre de 2026).
- **PMR446**: 446,0 – 446,2 MHz, uso común, **500 mW p. r. a.**, antena incorporada, solo portátiles, símplex, sin repetidores. 16 canales analógicos de 12,5 kHz desde 446,00625 MHz; digital en 6,25 kHz (dPMR) o 12,5 kHz (DMR). Corte de emisión a los 180 s (nota UN-110 y ECC/DEC/(15)05).
- **CB-27**: 26 960 – 27 410 kHz, **40 canales**, uso común **sin autorización desde el 11 de abril de 2015** (Orden IET/614/2015). **4 W** en FM y AM, **12 W p. c. e.** en BLU, antena de 6 dB como máximo y no directiva, sin amplificadores ni repetidores. **Canal 9**, socorro (nota UN-3).
- **433 MHz**: SRD de **10 mW p. r. a.** (1 mW sin condiciones), incluidos los LPD. **868 – 870 MHz**: SRD con ciclo de trabajo limitado; **500 mW** y 10 % en 869,400 – 869,650 MHz, donde funciona LoRa (notas UN-30 y UN-39).

## Autoevaluación

**1.** Quieres empezar a escuchar contactos de radioaficionados en 40 m. ¿Qué característica del receptor es imprescindible?

a) Que reciba FM estéreo  
b) Que tenga banda lateral única  
c) Que cubra la banda de 446 MHz  
d) Que tenga antena telescópica

??? success "Solución"
    **b)** La fonía de aficionado en HF se hace en BLU; con un receptor de AM solo oirás un ruido ininteligible. La FM estéreo es de radiodifusión en VHF, 446 MHz es la banda de PMR446 y la antena telescópica sirve, pero se mejora mucho con un hilo exterior.

**2.** Oyes en 9650 kHz una emisora internacional. ¿En qué banda de radiodifusión está?

a) 49 m  
b) 41 m  
c) 31 m  
d) 25 m

??? success "Solución"
    **c)** $\lambda = 300 / 9{,}65 \approx 31\ \text{m}$. Además, 9650 kHz está dentro de los márgenes de 9400 a 9900 kHz que el CNAF atribuye a la radiodifusión.

**3.** Con un receptor de banda ancha captas una conversación de un servicio profesional que no es de radiodifusión ni de aficionados. ¿Qué dice la Ley 11/2022?

a) Nada: escuchar sin transmitir siempre es libre.  
b) Que puedes escucharla, pero no grabarla.  
c) Que interceptar sin autorización comunicaciones no destinadas al público, y divulgar su contenido, es una infracción muy grave.  
d) Que solo es infracción si la comunicación iba cifrada.

??? success "Solución"
    **c)** Es lo que dice el artículo 106.15 de la Ley 11/2022. Interceptar y divulgar son dos conductas distintas, y las dos están tipificadas. La ley no distingue si la comunicación iba cifrada o no; el criterio es si está destinada al público en general.

**4.** ¿En qué frecuencia está el canal 5 analógico de PMR446?

a) 446,05000 MHz  
b) 446,05625 MHz  
c) 446,06250 MHz  
d) 446,03125 MHz

??? success "Solución"
    **b)** $446{,}00625 + (5 - 1) \cdot 0{,}0125 = 446{,}05625\ \text{MHz}$. La a) olvida que la primera portadora no está en el borde de la banda, sino a 6,25 kHz de él, y la c) suma cinco separaciones en lugar de cuatro.

**5.** Tienes autorización de radioaficionado y un portátil bibanda que transmite en 446 MHz con 5 W. ¿Puedes usarlo para hablar con unos amigos que llevan PMR446?

a) Sí, porque tienes autorización de radioaficionado.  
b) Sí, si bajas la potencia a 500 mW.  
c) No: la banda de PMR446 solo admite equipos PMR446, con antena incorporada y 500 mW como máximo.  
d) Sí, si usas el mismo subtono que ellos.

??? success "Solución"
    **c)** La nota UN-110 del CNAF exige equipos portátiles con antena incorporada que cumplan la norma EN 303 405. Tu autorización de radioaficionado solo cubre las bandas de aficionado, y 446,0 – 446,2 MHz no lo es para ese uso. Bajar la potencia no cambia que el equipo no sea un PMR446.

**6.** ¿Qué hace falta hoy en España para usar un equipo de CB-27 homologado?

a) Una autorización de la Jefatura Provincial de Inspección de Telecomunicaciones  
b) Aprobar el examen de radioaficionado  
c) Nada: es de uso común desde 2015  
d) Pagar una tasa anual

??? success "Solución"
    **c)** La Orden IET/614/2015 derogó el reglamento de la CB-27 de 2006 y la pasó a uso común. El artículo 19 del Real Decreto 123/2017 define el uso común como el que no precisa ningún título habilitante. Las condiciones están en la nota UN-3 del CNAF.

**7.** Un usuario de CB quiere montar en casa una antena directiva de 9 dB y un amplificador de 100 W para emitir en BLU. ¿Qué incumple de la nota UN-3 del CNAF?

a) Solo el amplificador  
b) Solo la antena  
c) Las dos cosas: la potencia pasa de 12 W p. c. e. y la antena supera 6 dB y es directiva  
d) Nada, porque en BLU no hay límite de potencia

??? success "Solución"
    **c)** La nota UN-3 limita la BLU a 12 W p. c. e., prohíbe acoplar dispositivos que den más potencia y exige antenas de 6 dB como máximo y sin directividad en el plano horizontal.

**8.** Un nodo LoRa emite en 869,525 MHz, sin técnicas de acceso al medio. ¿Cuánto tiempo puede transmitir como máximo en una hora?

a) 36 s  
b) 360 s  
c) 3,6 s  
d) Sin límite

??? success "Solución"
    **b)** 869,525 MHz está en la subbanda de 869,400 a 869,650 MHz, donde la nota UN-39 del CNAF permite 500 mW p. r. a. con un ciclo de trabajo del 10 %: $0{,}10 \cdot 3600 = 360\ \text{s}$. La a) es el 1 % de la subbanda de 868,000 a 868,600 MHz.
