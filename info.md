4 - 2 block
3 - 3 block
2 - 4 block
1 - 6 block

class barca:
    int lung
    char directie
    int, int primul block
    int block-distruse
    bool distrusa

ghicite[x][y] = {0 - default, 1 - impuscat nenimerit, 2 - impuscat nimerit}

tablaplayer1[x][y] = {0 - nimic, 1 - barca}
tablaplayer2[x][y] = {0 - nimic, 1 - barca}

Update game:
    Cerere catre server a noilor informatii

Stagii joc:
    1. Main menu + gasire joc (Client -> Server; PlayerID oponent sau nimic pentru un oponent random; Server -> Client; OK daca playerID trimite si el o cerere pentru clientul nostru sau un playerID random daca nu trimite un playerID si primeste si un gameID)
    2. Plasare barci (Client -> Server; Plasarea barcilor; Server -> Client; Trimite un ok cand ambii clienti au plasat barcile)
    3. Atacare pe rand (Daca nimeresti ataci iar) (Client -> Server; BlockID (Ex A1); Server -> Ambii client; Hit sau Miss (daca trimite hit clientul ghiceste iar))
    4. Casigator =  Primul care distruge toate barcile (Server -> Ambii clienti; Castigatorul)

