import random

def jogar():
    print("✨ Bem-vindo ao Grande Adivinhador Zaz! ✨")
    print("Estou pensando em um número entre 1 e 50...")
    
    numero_secreto = random.randint(1, 50)
    tentativas = 0
    ganhou = False
    
    while not ganhou:
        try:
            chute = int(input("\nDigite o seu palpite: "))
            tentativas += 1
            
            if chute < numero_secreto:
                print("Muito baixo! Tente um número maior.")
            elif chute > numero_secreto:
                print("Muito alto! Tente um número menor.")
            else:
                print(f"🎉 Parabéns! Você acertou o número secreto ({numero_secreto}) em {tentativas} tentativas!")
                ganhou = True
        except ValueError:
            print("Por favor, digite um número válido!")

if __name__ == "__main__":
    jogar()
