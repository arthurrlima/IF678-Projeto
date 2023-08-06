# IF678-Projeto
Projeto para a disciplina Infra Estrutura de Redes e Comunicação.
#Equipe 1
Arthur Romaguera Lima;
João Witor T. C. Santos;
Victor Vasconcelos Borges;
Heitor de Assis Machado;
Arthur Fernandes Scanoni;
Thays Cipriano;

Instrução de uso:
	1. As pastas sv_files e cl_files devem estar vazias, o programa criará os arquivos quando forem transmitidos.
 	2. rodar UDPServer.py
	3. rodar UDPClient.py ativará a criação da conexão e transferencia de arquivos. 
	ps: para mudar teste de arquivo .txt para .jpg (vice-versa) alterar file_name em UDPClient.py

demofile32.jpg made with p5js, para verificar, rodar script em https://editor.p5js.org/:

function setup() {
  
 let c = createCanvas(31, 31);
  background('white');
  
  noLoop();
  
  for(i= 0;i <=31; i+=2){
    for(j= 0;j <= 31; j+=2){
      
      let pick = random(0,2)
      
      if(pick <= 1){
        stroke('black')
        square(i, j, 1)
      }
    }
  }
  
  saveCanvas(c, 'Canvas', 'jpg');

}
