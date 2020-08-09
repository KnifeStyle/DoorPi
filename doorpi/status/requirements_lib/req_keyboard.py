import textwrap

REQUIREMENT = {
    "fulfilled_with_one": True,
    "text_description": textwrap.dedent("""\
        Die Aufgabe von einem Keyboard innerhalb von DoorPi ist es, Eingaben
        und Ausgaben zu steuern. Keyboard bezieht sich dabei nicht auf die
        Tastatur, sondern auf ein Brett mit Knöpfen und LEDs.  DoorPi ist in der
        Lage, mehrere Keyboards gleichzeitig zu verwalten. Dazu muss in der
        Konfiguration zuerst eine Zuordnung getroffen werden, welchen frei
        ausgedachten, aber eindeutigen Namen das Keyboard bekommmt
        (``KeyboardName``) und von welchem Typ das Keyboard ist.  Diese
        Zuordnung findet in einer Konfigurations-Sektion "keyboards" statt.
        Danach kann jedes Keyboard drei weitere Sektionen besitzen:

        1. allgemeine und Keyboard-spezifische Konfigurationsparameter
           (Sektionsname ``keyboard_settings_[KeyboardName]``)
        2. Auflistung der InputPins (Sektionsname
           ``keyboard_input_[KeyboardName]``), wobei Pin auch eine Zeichenkette
           sein kann wie im Beispiel vom RFID-Reader.
        3. Auflistung der OutputPins (Sektionsname
           ``keyboard_output_[KeyboardName]``) mit Pinnummer und sprechendem
           Namen

        Der sprechende Name muss eindeutig sein und wird später genutzt, um die
        Pins in Actions anzusprechen.

        Beispiel (alles nach einem # sind Kommentare)::

            virtuelles = filesystem
            rfid = rdm6300

            [keyboard_settings_virtuelles]
            # Pfad, in dem dann die Input-Dateien zu finden sind
            base_path_input = !BASEPATH!/keyboards/virtuelles/inputpins
            # Pfad, in dem dann die Output-Dateien zu finden sind
            base_path_output = !BASEPATH!/keyboards/virtuelles/outputpins
            # Ausgangszustand der Eingabe-Datei soll wiederhergestellt werden,
            # wenn Signal erkannt wurde
            reset_input = true

            [keyboard_input_virtuelles]
            # Wenn diese Datei eine '1' beinhaltet, dann soll ein Ausgang mit
            # dem Namen tueroeffner gesteuert werden
            klingel = out:tueroeffner:0,1,3

            [keyboard_output_virtuelles]
            # Die Datei "ausgang" wird im Dateisystem angelegt, aber innerhalb
            # von DoorPi mit "tueroeffner" angesprochen
            ausgang = tueroeffner
            # Die Datei "ausgang2" wird im Dateisystem angelegt, aber innerhalb
            # von DoorPi mit "fensteroeffner" angesprochen
            ausgang2 = fensteroeffner

            [keyboard_settings_rfid]
            # Der Port, mit dem der Reader verbunden ist, muss immer mit
            # angegeben werden.
            port = /dev/ttyAMA0

            [keyboard_input_rfid]
            1234567 = out:tueroeffner,1,0,3
            2345678 = out:fensteroeffner,1,0,3

            # Eine Sektion [keyboard_output_rfid] hat keinen Sinn, da ein
            # RFID-Reader nichts ausgeben kann.

        Ergebnis des Beispiels ist, dass:

        1. zwei Keyboards innerhalb von DoorPi registiert werden - das eine
           dateibasierend mit dem Namen "virtuelles", das andere ein RFID-Reader
           mit dem Namen "rfid"
        2. dem virtuellen Keyboard alle nötigen Parameter mitgegeben werden,
           beim rfid Keyboard nur die Default-Parameter genutzt werden.
        3. ein InputPin für das virtuelle Keyboard angelegt wird
        4. wenn die Datei ``!BASEPATH!/keyboards/virtuelles/inputpins/klingel``
           eine 1 als Inhalt bekommt, wird

           - Ausgang tueroeffner (in dem Fall die Datei
             ``!BASEPATH!/keyboards/virtuelles/outputpins/ausgang``)
           - neu geschrieben und bekommt den Inhalt "1"
           - es wird drei Sekunden gewartet
           - und die Datei wird neu geschrieben, diesmal mit dem Inhalt "0"
        5. ähnliches für das rfid Keyboard definiert wurde:

           - der RFID-Chip mit dem Code "1234567" öffnet den tueroeffner
           - der RFID-Chip mit dem Code "2345678" öffnet den fensteroeffner

        Wobei ``!BASEPATH!`` für das Home-Verzeichnis von DoorPi steht.
        """),
    "libraries": {
        "pifacedigitalio": {
            "text_warning": textwrap.dedent("""\
                Neben der reinen Installation des Python-Moduls
                ``pifacedigitalio`` ist es auch wichtig, SPI am System zu
                aktivieren (siehe Links).  Außerdem muss bei Bestellungen darauf
                geachtet werden, dass es zwei Versionen gibt:

                * `PiFace digital 1`__
                * `PiFace digital 2`__

                __ https://www.rasppishop.de/Piface-Digital-Erweiterung-fuer-Raspberry-Pi
                __ https://www.rasppishop.de/PiFace-Digital-2-Erweiterungsplatine-/-Modul-fuer-den-Raspberry-Pi-Modell-B-
                """),
            "text_description": (
                'Das Python-Modul pifacedigitalio ist der "Treiber" für die'
                " PiFace-Hardware."),
            "auto_install": False,
            "text_test": (
                "Der Status kann gestestet werden, indem im Python-Interpreter"
                " ``import pifacedigitalio`` eingeben wird."),
            "text_links": {
                "docs.python.org": (
                    "https://docs.python.org/library/configparser.html"),
                "PiFace Beschreibung auf piface.org.uk": (
                    "http://www.piface.org.uk/products/piface_digital/"),
                "Installationsanleitung auf GitHub": \
                    "http://piface.github.io/pifacedigitalio/installation.html",
                "SPI und I²C aktivieren": (
                    "http://raspberry.tips/faq"
                    "/raspberry-pi-spi-und-i2c-aktivieren/"),
            }
        },
        "RPi.GPIO": {
            "text_description": (
                "RPi.GPIO kümmert sich um die Ein- und Ausgaben der"
                " GPIO-Schnittstelle eines Raspberry Pi."),
            "text_installation": (
                "Das Modul ist im Paket ``python3-rpi.gpio`` (Raspbian) bzw. im"
                " AUR-Paket ``python-rpi.gpio`` (Arch Linux ARM) enthalten."),
            "auto_install": False,
            "text_test": (
                "Der Status kann gestestet werden, indem im Python-Interpreter"
                " ``import RPi.GPIO`` eingeben wird."),
            "text_links": {
                "www.raspberrypi.org": {
                    "GPIO Overview": (
                        "https://www.raspberrypi.org/documentation"
                        "/hardware/raspberrypi/gpio/README.md"),
                    "GPIO Usage": (
                        "https://www.raspberrypi.org/documentation"
                        "/usage/gpio/README.md"),
                },
                "RPi.GPIO on pypi": "https://pypi.python.org/pypi/RPi.GPIO",
                "Installationsanleitung auf Sourceforge": (
                    "http://sourceforge.net/p/raspberry-gpio-python"
                    "/wiki/install/"),
            }
        },
        "serial": {
            "text_description": textwrap.dedent("""\
                Hier die Beschreibung aus der ``from_rdm6300.py``, die
                `msmolny`__ netterweise erstellt hat:

                __ https://github.com/msmolny

                Configuration
                -------------

                1. Define a new keyboard of type 'rdm6300'
                2. Define inputPins section for that keyboard
                3. Each RFID tag has a decimal number printed
                   on the surface. This is the Input PIN number.
                   Define this number and an appropriate action.

                Sample:

                [keyboards]
                rfidreader = rdm6300
                ...
                [rfidreader_InputPins]
                1234567 = out:Tueroeffner,1,0,3
                2345678 = out:Tueroeffner,1,0,3

                That's all...

                Hardware Connections
                --------------------

                RDM6300 Pin Layout

                ::

                      +-------------------------+
                      |                         |
                      | (1) ANT1                |
                      | (2) ANT2                |
                      | P2                      |
                      |                         |
                      |                         |
                      |                         |
                      |                     P1  |
                      |             +5V(DC) (5) |
                      | P3              GND (4) |
                      | (3) GND             (3) |
                      | (2) +5V(DC)      RX (2) |
                      | (1) LED          TX (1) |
                      |                         |
                      +-------------------------+

                Connect one of the two +5V(DC) and one of the two GND to 5V (Pin
                2 on the RaspberryPi Board) and to GND (Pin 6 on the RaspberryPi
                Board). As I used a ribbon cable, the simplest way was to
                connect to (4) and (5) of P1 from the RDM6300.

                Then, connect TX (pin (1) of P1) to RXD from the UART (Pin 10 on
                the RaspberryPi Board) - BUT NOT DIRECTLY, OTHERWISE YOU MIGHT
                DAMAGE YOUR RASPBERRY PI!!!  The RaspberryPi expects 3,3V level
                on the UART Pins, but the RDM6300 delivers 5V.

                Simplest solution for this is a voltage divider via resistors::

                    RDM6300 P1(1) ----------+
                                            |
                                       Resistor R1
                                            |
                    RasPi Board (Pin 10) ---+
                                            |
                                        Resistor R2
                                            |
                    GND --------------------+

                Ideal solution: R1=5k, R2=10k, this will deliver exactly 3,3V
                to RasPi Board(Pin 10).

                Alternative solution: As most RaspberryPi bundles only contain
                10k resistors, you might either use 2 10k resistors in parallel
                to get a 5k resistor, or simply use 10k for R1 instead.
                R1=R2=10k will deliver 2,5V to RasPi Board(Pin 10), but that
                works also.

                Reference: I used this resource to learn how to work with
                RDM6300, how to connect it to the RaspberryPi and how to handle
                RFID data: <http://kampis-elektroecke.de/?page_id=3248>
                """),
            "text_installation": (
                "Das Modul ist im Paket ``python3-serial`` (Raspbian) bzw."
                " ``python-pyserial`` (Arch Linux ARM) enthalten."),
            "auto_install": False,
            "text_test": (
                "Der Status kann gestestet werden, indem im Python-Interpreter"
                " ``import serial`` eingeben wird."),
            "text_links": {
                "serial @ pypi": "https://pypi.python.org/pypi/serial",
            },
        },
        "watchdog": {
            "text_warning": (
                "Häufiges Schreiben auf SD-Karten fördert deren Verschleiß!"
                " Deshalb sollten Pfade unter ``/run/doorpi`` verwendet werden,"
                " weil diese im Arbeitsspeicher des Pi verbleiben."),
            "text_description": textwrap.dedent("""\
                Das Python-Modul ``watchdog`` wird genutzt, um ein
                dateibasierendes Keyboard zu erstellen.  So können entweder zu
                Testzwecken ohne Hardware-Aufbau Events und Actions getestet
                werden oder es kann als Schnittstelle zu anderen Systemen
                dienen, die per SSH-Befehle die Dateien schreiben und lesen, die
                auch vom virtuellen keyboard verarbeitet werden.  Dabei kann
                eingestellt werden, in welchem Ordner die Dateien liegen, die
                jeweils als Ein- und Ausgabe fungieren und ob die Eingabedateien
                nach Erkennung eines Events durch das Filesystem-Keyboard wieder
                zurück in den Ausgangszustand versetzt werden.
                """),
            "text_installation": (
                "Das Modul ist im Paket ``python3-watchdog`` (Raspbian) bzw."
                " ``python-watchdog`` (Arch Linux ARM) enthalten."),
            "auto_install": False,
            "text_test": (
                "Der Status kann gestestet werden, indem im Python-Interpreter"
                " ``import watchdog`` eingeben wird."),
            "text_links": {
                "watchdog @ pypi": "https://pypi.python.org/pypi/watchdog",
            },
        },
    },
}
