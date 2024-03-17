# TgTools

![](https://i.imgur.com/kx0dIHG.png)

Some TgTools for Telegram!

You can find the explanation of the code [here!]([https://ethicalhacking.freeflarum.com/](https://ethicalhacking.freeflarum.com/d/1103-tgtools-telegram-automatizzato))

In questa repo ci sono vari tools per Telegram molto utili.
- **AddUserGroup.py**: Permette di aggiungere membri a un gruppo Telegram da un file CSV contenente i  membri. Gli utenti possono essere aggiunti tramite username o ID utente.
- **AddUsers.py**: Simile al precedente ma permette di aggiungere membri utilizzando una struttura e una sintassi diverse. Chiede all'utente di selezionare il gruppo e il metodo di aggiunta (per username o ID utente).
- **WhoIsHere.py**: Estrae i membri da un gruppo Telegram e li salva in un file CSV, quindi si seleziona il gruppo da cui si vuole estrarre i membri e vengono salvati in un file CSV.
- **spammer.py**: Consente di inviare messaggi tramite file CSV, chiede all'utente il messaggio da inviare e invia il messaggio a ciascun contatto sfruttando l'API di Telegram.



### Installazione:

\ `apt install git -y`

\ `git clone https://github.com/Samueleex/TgTools`

\ `cd TgTools`

\ `chmod +x * && python3 setup.py`



### Esecuzione tools:

\ `python3 nome.py`



### CSV gen:

\ `python3 WhoIsHere.py` (si salverà su members.csv)
\ `python3 AddUsers.py`

Oppure:

\ `python3 AddUserGroup.py members.csv`
