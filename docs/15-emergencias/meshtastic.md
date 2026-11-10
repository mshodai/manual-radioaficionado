# Meshtastic

!!! warning "Fuera de la radioafición"
    Meshtastic usa LoRa en la banda de uso común de 868 MHz; no es un servicio de radioaficionados. A esa banda se la suele llamar «banda ISM», pero en Europa no lo es: ISM (*industrial, scientific and medical*) es la sigla inglesa de las bandas ICM, destinadas a aplicaciones industriales, científicas y médicas, como la de 433 MHz del [capítulo 14](../14-escucha-uso-libre.md#433-mhz). La de 868 MHz es de dispositivos de corto alcance.

Meshtastic se ha hecho muy popular como «radio de emergencia» barata: un módulo del tamaño de una caja de cerillas, una antena pequeña y el móvil para escribir. En esta sección aprenderás qué es, en qué banda funciona en España y con qué límites, por qué no es radioafición aunque la usen muchos radioaficionados, qué pasa con el cifrado según la banda y qué puede y qué no puede hacer cuando falla todo lo demás. Te servirá para valorarla como complemento de tu plan de comunicaciones sin confundirla con él.

## Qué es

**Meshtastic** es un proyecto de código abierto que convierte radios LoRa de bajo coste en una plataforma de comunicación de largo alcance, sin red, para zonas sin infraestructura de comunicaciones o con una infraestructura poco fiable. Así lo presenta su [documentación oficial](https://meshtastic.org/docs/introduction/), que destaca tres cosas: no hace falta el móvil para que la malla funcione, no hace falta ningún encaminador central y los miembros de la malla se envían mensajes de texto (comprobado en noviembre de 2026).

Cada equipo de la red es un **nodo**: una placa con un microcontrolador y una radio LoRa, normalmente alimentada por una batería pequeña. Lo habitual es escribir los mensajes en el móvil, que se conecta al nodo por Bluetooth, aunque algunos nodos traen pantalla y teclado propios.

La red es una **malla** (*mesh*): no hay estación central, y cada nodo retransmite lo que oye para que llegue más lejos. Según la [descripción técnica de Meshtastic](https://meshtastic.org/docs/overview/), el reenvío funciona así (comprobado en noviembre de 2026):

1. El nodo que recibe un paquete descarta los duplicados.
2. Si el **límite de saltos** del paquete no ha llegado a cero, espera un tiempo aleatorio, más corto cuanto peor oye al emisor, de modo que retransmiten antes los nodos más alejados.
3. Si mientras espera oye a otro nodo retransmitir el mismo paquete, normalmente renuncia a hacerlo él. La documentación llama a este sistema **inundación gestionada** (*managed flooding*).
4. Cada retransmisión resta uno al límite de saltos.

El límite de saltos es **3 por defecto y 7 como máximo**, según la [página de configuración de LoRa](https://meshtastic.org/docs/configuration/radio/lora/) (comprobado en noviembre de 2026). Con tres saltos, un mensaje puede llegar a nodos que están a cuatro enlaces de distancia del emisor, pero no más allá.

El firmware se publica con licencia **GPL-3.0** en el [repositorio oficial del proyecto](https://github.com/meshtastic/firmware). Su [lista de versiones](https://github.com/meshtastic/firmware/releases) da como última estable la **2.7.26**, publicada el 24 de junio de 2026, y como última de pruebas la 2.8.2 *alfa*, del 4 de noviembre de 2026 (comprobado en noviembre de 2026). El proyecto avanza deprisa: antes de configurar un nodo, mira qué versión hay y lee sus notas.

## LoRa en 868 MHz

**LoRa** es una modulación de espectro ensanchado: reparte la señal en un ancho de banda mucho mayor del que necesitarían los datos y, a cambio, se recibe con señales muy débiles, por debajo incluso del nivel de ruido. Sacrifica velocidad para ganar alcance.

En Europa, Meshtastic usa la región **EU_868**. Su [documentación de ajustes de radio](https://meshtastic.org/docs/overview/radio-settings/) dice que trabaja de **869,40 a 869,65 MHz**, con un único canal centrado en **869,525 MHz**, una potencia máxima de **+27 dBm p. r. a.** y un **ciclo de trabajo del 10 %** (comprobado en noviembre de 2026). Esos números no son una elección del proyecto: son los de la subbanda de 869,400 a 869,650 MHz de la nota UN-39 del CNAF, que viste en el [capítulo 14](../14-escucha-uso-libre.md#868-mhz-y-lora). Comprueba que +27 dBm son los 500 mW de la nota:

$$
P = 10^{27/10}\ \text{mW} \approx 500\ \text{mW}
$$

El firmware cuenta el tiempo de emisión en una hora móvil y, al llegar al 10 %, **deja de transmitir** hasta que vuelve a estar por debajo. Hay una opción para saltarse ese límite, pero la propia documentación avisa de que con ella puedes incumplir la normativa (comprobado en noviembre de 2026). No la actives.

### Cuánto se puede transmitir

Todos los nodos tienen que usar el mismo **preajuste de módem** para entenderse. El de fábrica es **LONG_FAST**: factor de ensanchamiento 11, 250 kHz de ancho de banda y una velocidad máxima teórica de **1,07 kbit/s**, que según la misma documentación no tiene en cuenta las cabeceras, los saltos ni las retransmisiones (comprobado en noviembre de 2026).

**Ejemplo.** Un mensaje de texto largo, de 200 bytes, son $200 \cdot 8 = 1600$ bits. A 1,07 kbit/s ocupa el canal durante al menos

$$
t = \frac{1600\ \text{bit}}{1070\ \text{bit/s}} \approx 1{,}5\ \text{s}
$$

Con el 10 % de una hora, 360 s, un nodo podría enviar como mucho unos $360 / 1{,}5 = 240$ mensajes así por hora, y bastantes menos en la práctica, porque cada nodo también gasta su tiempo en retransmitir los mensajes de los demás, en anunciar su posición y en enviar datos de su batería. Y el canal es **uno solo para todos**: mientras un nodo transmite, los que lo oyen esperan. Una malla con muchos nodos activos se satura mucho antes de que ninguno llegue a su 10 %.

## Por qué no es radioafición

La radioafición no se define por quién maneja el equipo, sino por la **banda** y la **autorización**. El artículo 2 de la [Orden IET/1311/2013](https://www.boe.es/buscar/act.php?id=BOE-A-2013-7624#a2) llama uso especial del espectro por radioaficionados al uso de las bandas que el CNAF atribuye al servicio de aficionados, con fines de instrucción individual, intercomunicación o estudios técnicos (comprobado en noviembre de 2026). La subbanda de 869,4 a 869,65 MHz no es una de ellas: es una banda de **uso común** para dispositivos de corto alcance, sin título habilitante, como viste en el [capítulo 14](../14-escucha-uso-libre.md#otras-bandas-de-uso-comun).

De ahí salen tres consecuencias:

- **Cualquiera** puede usar Meshtastic en 868 MHz, con o sin examen, siempre que el equipo cumpla las condiciones de la nota UN-39.
- Un radioaficionado que lo usa en 868 MHz no está operando como radioaficionado: es un usuario más de una banda de uso común. Su autorización no le da más potencia ni le permite cambiar las condiciones.
- Lo que hagas en Meshtastic **no cuenta** como actividad de radioaficionado, ni la colaboración con Protección Civil que prevé la orden se hace por ahí: la orden habla de tus medios **en las bandas de aficionado**, como viste en la [página principal del capítulo](index.md#lo-que-dice-la-orden).

## El cifrado según la banda

### En 868 MHz

Meshtastic cifra los mensajes de cada canal con **AES**, usando la clave del canal: una clave de 16 bytes da AES-128 y una de 32 bytes, AES-256. Pero la documentación de [cifrado](https://meshtastic.org/docs/overview/encryption/) hace varias advertencias (comprobado en noviembre de 2026):

- El **canal primario por defecto** usa una clave que está **publicada**. Todo lo que envíes en él lo puede leer cualquiera.
- La **cabecera** de los paquetes nunca se cifra, porque los nodos la necesitan para retransmitir mensajes que no saben descifrar.
- En el modo de cifrado de canal clásico, quien tenga la clave puede enviar mensajes haciéndose pasar por otro usuario del canal, según la página de [limitaciones del cifrado](https://meshtastic.org/docs/about/overview/encryption/limitations/).

Los **mensajes directos** entre dos nodos usan desde la versión 2.5 una clave que solo comparten esos dos nodos, acordada con criptografía de clave pública (comprobado en noviembre de 2026).

### En las bandas de aficionado

Meshtastic tiene un **modo con licencia** (*licensed mode*) para radioaficionados. Al activarlo, la [configuración de usuario](https://meshtastic.org/docs/configuration/radio/user/) pide poner el **indicativo** como nombre del nodo y dejar vacía la clave del canal, lo que **elimina el cifrado**; los nodos en ese modo envían todo sin cifrar y firman los paquetes que caben (comprobado en noviembre de 2026). Solo en ese modo deja elegir las regiones de aficionado, como **ITU1_2M** (144 a 146 MHz) e **ITU1_70CM** (430 a 440 MHz), según la [página de configuración de LoRa](https://meshtastic.org/docs/configuration/radio/lora/) (comprobado en noviembre de 2026).

La documentación de Meshtastic justifica esas reglas con la normativa de EE. UU., que aquí no vale. En España, la base es el artículo 30.2 de la [Orden IET/1311/2013](https://www.boe.es/buscar/act.php?id=BOE-A-2013-7624#a30), que prohíbe codificar las transmisiones entre estaciones de aficionado para ocultar su significado, y el artículo 29 de la Orden IET/1311/2013, que te obliga a identificarte al principio y al final de cada emisión y al menos cada diez minutos en las largas (comprobado en noviembre de 2026). Antes de montar una malla en 2 m o 70 cm, piensa además en tres cosas:

- Un nodo que retransmite solo, sin nadie delante, se parece mucho a una **estación automática desatendida**, que la orden solo autoriza como estación colectiva de una asociación, con sus propias condiciones ([capítulo 9](../09-reglamentacion/espanol.md#estaciones-automaticas-desatendidas)). Si dudas, pregunta a tu Jefatura Provincial.
- Tiene que respetar el **plan de bandas** de la IARU para esa banda ([capítulo 9](../09-reglamentacion/index.md#los-planes-de-2-m-y-70-cm)).
- Los modos con y sin licencia **no se entienden entre sí**, y Meshtastic no prevé que lleguen a hacerlo, según sus [preguntas frecuentes](https://meshtastic.org/docs/faq/) (comprobado en noviembre de 2026). Una malla de aficionados en 70 cm no habla con la malla pública de 868 MHz.

!!! tip "Para el examen"
    Lo que se pregunta no es Meshtastic, sino la regla de fondo: **en las bandas de aficionado no se puede cifrar** (artículo 30.2 de la Orden IET/1311/2013), y en las de uso común rigen las condiciones del CNAF, no las de la orden. El mismo equipo puede estar en un régimen o en otro según la frecuencia en que transmite.

## Lo que puede y lo que no puede hacer en una emergencia

Meshtastic tiene ventajas reales: cuesta poco, gasta muy poca batería, no necesita autorización y cualquier persona aprende a usarlo en minutos. Para avisar a la familia de que estás bien dentro de un barrio, o para coordinar un grupo pequeño en el monte, puede servir. Pero conviene conocer sus límites antes de confiar en él:

- **Solo texto corto.** Las aplicaciones limitan cada mensaje a unos **200 bytes** (comprobado en noviembre de 2026). No hay voz.
- **Poca capacidad.** Como has calculado, el canal es lento y compartido. En una emergencia, cuando todo el mundo escribe a la vez, la malla se congestiona justo cuando más falta hace. La documentación recomienda espaciar los envíos automáticos de posición y de telemetría para no agotar el ciclo de trabajo.
- **Alcance de visión directa.** A 868 MHz la señal no rodea montañas ni edificios, como viste con el horizonte radioeléctrico en el [capítulo 5](../05-propagacion-bandas.md#vision-directa-y-horizonte-radioelectrico). El alcance depende de que haya nodos en sitios altos, que normalmente instalan particulares y nadie garantiza que funcionen tras un temporal o un apagón largo.
- **Depende del móvil.** Aunque la malla funcione sin él, la mayoría de los usuarios escriben con el móvil, que también hay que cargar.
- **Sin entrega garantizada.** Más allá del límite de saltos, el mensaje no llega, y en una malla saturada se pierden paquetes.
- **No es un canal oficial.** Ni el 112 ni los servicios de emergencia escuchan Meshtastic. No sustituye a una llamada de socorro ni a una red organizada.
- **Privacidad.** El canal por defecto es legible por cualquiera, y si activas el envío de posición, todos los nodos sabrán dónde estás.

!!! example "En la práctica"
    Si quieres usar Meshtastic en tu plan familiar, trátalo como una vía más, no como la principal. Acordad un canal propio con una clave que no esté publicada, decidid qué mensajes vais a mandar (por ejemplo, «estoy bien» y el lugar de encuentro acordado) y comprobadlo de vez en cuando, como cualquier otra parte del plan de la [página principal del capítulo](index.md#el-plan-de-comunicaciones).

## Resumen

- **Meshtastic** es una red de mensajería de texto en malla sobre **LoRa**, de código abierto (GPL-3.0). Cada nodo retransmite lo que oye; el límite de saltos es **3 por defecto y 7 como máximo**. Última versión estable comprobada: **2.7.26** (24 de junio de 2026).
- En Europa usa la región **EU_868**: **869,40 – 869,65 MHz**, canal en **869,525 MHz**, **+27 dBm (500 mW) p. r. a.** y **10 %** de ciclo de trabajo, las condiciones de la nota UN-39 del CNAF para esa subbanda.
- **No es radioafición**: la banda de 868 MHz es de uso común, sin autorización, y la orden de radioaficionados no se aplica en ella.
- En 868 MHz puede cifrar, pero el canal por defecto usa una **clave publicada**. En las bandas de aficionado, el **modo con licencia** quita el cifrado y usa el indicativo, como exige en España el artículo 30.2 de la Orden IET/1311/2013.
- En una emergencia es un complemento: **solo texto**, poca capacidad, alcance de visión directa, sin entrega garantizada y **sin conexión con el 112**.

## Autoevaluación

**1.** ¿Por qué un radioaficionado que usa Meshtastic en 869,525 MHz no está operando como radioaficionado?

a) Porque Meshtastic no permite poner el indicativo.  
b) Porque esa frecuencia no está en una banda atribuida al servicio de aficionados, sino en una de uso común.  
c) Porque la potencia es demasiado baja para ser radioafición.  
d) Porque los mensajes de texto no se consideran radioafición.

??? success "Solución"
    **b)** Lo que define la radioafición es el uso de las bandas que el CNAF atribuye al servicio de aficionados, con autorización (artículo 2 de la Orden IET/1311/2013). La subbanda de 869,4 a 869,65 MHz es de uso común para dispositivos de corto alcance. La potencia y el tipo de mensaje no tienen nada que ver: hay radioaficionados que trabajan con 1 W y modos de texto.

**2.** Un nodo Meshtastic europeo transmite a +27 dBm. ¿A cuántos milivatios equivale?

a) 27 mW  
b) 270 mW  
c) 500 mW  
d) 1000 mW

??? success "Solución"
    **c)** $10^{27/10} = 10^{2{,}7} \approx 501$ mW, es decir, 500 mW: el máximo de la nota UN-39 para la subbanda de 869,400 a 869,650 MHz. Cada 10 dB multiplican por 10 y cada 3 dB, por 2 aproximadamente: 20 dBm son 100 mW, y 7 dB más (10 dB menos 3 dB) son unas cinco veces más.

**3.** Con el preajuste LONG_FAST (1,07 kbit/s teóricos), ¿cuánto ocupa el canal como mínimo un mensaje de 100 bytes?

a) Unos 0,09 s  
b) Unos 0,75 s  
c) Unos 1,5 s  
d) Unos 7,5 s

??? success "Solución"
    **b)** 100 bytes son 800 bits, y $800 / 1070 \approx 0{,}75$ s. Es un mínimo: la cabecera del paquete y cada retransmisión en la malla añaden tiempo. La c) es la de un mensaje de 200 bytes.

**4.** Activas el modo con licencia de Meshtastic para usarlo en 70 cm. ¿Qué cambia en el cifrado y por qué?

a) Nada: el cifrado es obligatorio en todas las bandas.  
b) Se elimina el cifrado del canal, porque en las bandas de aficionado está prohibido codificar las transmisiones para ocultar su significado.  
c) Se pasa a AES-256, más seguro, porque la potencia es mayor.  
d) Se cifra solo la cabecera.

??? success "Solución"
    **b)** En España lo prohíbe el artículo 30.2 de la Orden IET/1311/2013. El modo con licencia pide dejar vacía la clave del canal y poner el indicativo como nombre. La d) es al revés: la cabecera no se cifra nunca, en ningún modo.

**5.** ¿Cuál de estas afirmaciones sobre Meshtastic en una emergencia es correcta?

a) Sustituye al 112 cuando no hay cobertura de móvil.  
b) Garantiza la entrega de los mensajes gracias a la malla.  
c) Es útil para mensajes de texto cortos en un área pequeña, pero se congestiona con muchos usuarios y no conecta con los servicios de emergencia.  
d) Permite enviar voz a varios kilómetros sin autorización.

??? success "Solución"
    **c)** Es una herramienta complementaria. Nadie de los servicios de emergencia escucha Meshtastic (a), un mensaje que supera el límite de saltos o que se pierde en una malla saturada no llega (b), y solo transmite texto (d).

**6.** Estás en el canal primario por defecto de Meshtastic. ¿Quién puede leer tus mensajes?

a) Solo los nodos de tu familia.  
b) Nadie, porque están cifrados con AES.  
c) Cualquiera que tenga un nodo Meshtastic al alcance de la malla, porque la clave por defecto está publicada.  
d) Solo los radioaficionados con modo con licencia.

??? success "Solución"
    **c)** El cifrado solo protege si la clave es secreta, y la del canal primario por defecto la publica el propio proyecto. Para un canal privado hay que crear una clave nueva y compartirla solo con quien deba usarla. La d) no tiene sentido: los modos con y sin licencia ni siquiera se entienden entre sí.
