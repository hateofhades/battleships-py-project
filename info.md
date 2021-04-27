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
    1. Main menu + gasire joc
    2. Plasare barci
    3. Atacare pe rand (Daca nimeresti ataci iar)
    4. Casigator =  Primul care distruge toate barcile