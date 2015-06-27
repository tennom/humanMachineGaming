#include "defs.h"
#include "MySocket.h"

double ***readPayoffMatrixFromFile(int _A[2], const char *game);
void printGame(int _A[2], double ***_M);
void cleanPayoffMatrix(double ***_M, int _A[2]);

void runGame(double ***M, int A[2], int iters);

bool cheapTalk = false;

/* **************************************
//
//  ./CheapTalk [game] [iters] [cheaptalk]
//
// ************************************** */
int main(int argc, char *argv[]) {
    if (argc < 3) {
        printf("not enough commandline parameters\n");
        exit(1);
    }

    // read in the game file
	double ***M;
	int A[2];
    int iters = atoi(argv[2]);
    printf("iters = %i\n", iters);
    if (argc > 3) {
        if (!strcmp(argv[3], "cheaptalk")) {
            cheapTalk = true;
            printf("cheapTalk = true\n");
        }
    }
    M = readPayoffMatrixFromFile(A, argv[1]);


    runGame(M, A, iters);

    cleanPayoffMatrix(M, A);

    return 0;
}

void runGame(double ***M, int A[2], int iters) {
    int i, j;
    int acts[2];
    char talk[2][1024];
    char nombres[2][1024];
    char buf[1024];
    double sum[2] = {0.0, 0.0};

    // get connections
    MySocket *coms[2];
    for (j = 0; j < 2; j++) {
        coms[j] = new MySocket(3000+j);
        coms[j]->AcceptEm();
        coms[j]->ReadMessage(nombres[j]);
        printf("name: %s\n", nombres[j]);
    }
    
    strcpy(buf, "Go");
    for (j = 0; j < 2; j++) {
        coms[j]->SendMessage(buf, strlen(buf));
    }
    
    for (i = 0; i < iters; i++) {
        if (cheapTalk) {
            //printf("Reading messages:\n");
            for (j = 0; j < 2; j++) {
                coms[j]->ReadMessage(talk[j]);
                //printf("%i: %s\n", j, talk[j]);
            }
            
            //printf("Sending messages:\n");
            for (j = 0; j < 2; j++) {
                //printf("%s\n", talk[1-j]);
                coms[j]->SendMessage(talk[1-j], strlen(talk[1-j]));
            }
        }
    
        for (j = 0; j < 2; j++) {
            coms[j]->ReadMessage(buf);
            acts[j] = atoi(buf);
        }

        printf("%i: (%i, %i) -> %.2lf, %.2lf\n", i, acts[0], acts[1], M[0][acts[0]][acts[1]], M[1][acts[0]][acts[1]]);
        
        sprintf(buf, "%i %i $", acts[0], acts[1]);
        for (j = 0; j < 2; j++) {
            coms[j]->SendMessage(buf, strlen(buf));
            sum[j] += M[j][acts[0]][acts[1]];
        }
    }
    
    printf("\nAverages: %lf, %lf\n", sum[0] / iters, sum[1] / iters);
    
    //usleep(2000000);
    
    delete coms[0];
    delete coms[1];

}

double ***readPayoffMatrixFromFile(int _A[2], const char *game) {
	double ***_M;
    
	char filename[1024];
	sprintf(filename, "..//..//games//%s.txt", game);
	
	FILE *fp = fopen(filename, "r");
	if (fp == NULL) {
		// check in an alternate directory before giving up
		sprintf(filename, "..//games//%s.txt", game);
		fp = fopen(filename, "r");
		if (fp == NULL) {
			printf("file %s not found\n", filename);
			exit(1);
		}
	}

	fscanf(fp, "%i", &(_A[0]));
	fscanf(fp, "%i", &(_A[0]));
	fscanf(fp, "%i", &(_A[1]));
	
	int i, j;
	_M = new double**[2];
	for (i = 0; i < 2; i++) {
		_M[i] = new double*[_A[0]];
		for (j = 0; j < _A[0]; j++)
			_M[i][j] = new double[_A[1]];
	}

	for (i = 0; i < _A[1]; i++) {
		for (j = 0; j < _A[0]; j++) {
			fscanf(fp, "%lf %lf", &(_M[0][j][i]), &(_M[1][j][i]));
		}
	}
    
    printf("game: %s\n", game);
    printGame(_A, _M);
    
	return _M;
}

void printGame(int _A[2], double ***_M) {
    int i, j;
    
    printf("\n   |      ");
    
    for (i = 0; i < _A[1]; i++)
        printf("%i      |      ", i);
    printf("\n");
    for (i = 0; i < _A[0]; i++) {
        printf("--------------------------------------\n %i | ", i);
        for (j = 0; j < _A[1]; j++) {
            printf("%.2lf , %.2lf | ", _M[0][i][j], _M[1][i][j]);
        }
        printf("\n");
    }
    printf("--------------------------------------\n\n");
}

void cleanPayoffMatrix(double ***_M, int _A[2]) {
	int i, j;
	
	for (i = 0; i < 2; i++) {
		for (j = 0; j < _A[0]; j++)
			delete _M[i][j];
		delete _M[i];
	}
	delete _M;
}
