import pygame
import subprocess
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((400, 200))
pygame.display.set_caption("Changement de mode - Appuie sur ESPACE")

# Dictionnaire des scripts
modes = {
    1: "pianoNormal.py",
    2: "metastairsAccordAvecVolume.py",
    3: "finalShepard.py"
}

idx = 1
process = None

font = pygame.font.SysFont(None, 24)

def afficher_texte(text):
    screen.fill((0, 0, 0))
    surface = font.render(text, True, (255, 255, 255))
    screen.blit(surface, (20, 80))
    pygame.display.flip()

print("Heure de demarrage :", datetime.now().strftime("%H:%M:%S"))

try:
    running = True
    while running:
        script = modes.get(idx)
        if script:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] → Lancement de : {script}")
            afficher_texte(f"Mode {idx}: {script}")
            try:
                process = subprocess.Popen(["python3", script])
            except Exception as e:
                print(f"Erreur au lancement de {script} : {e}")
        else:
            print(f"Script {idx} non trouve.")
            afficher_texte(f"Script {idx} non trouve.")

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

        # Interruption du processus courant
        if process and process.poll() is None:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] → Interruption de : {script}")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Forçage de l'arret...")
                process.kill()

        # Mode suivant
        idx = idx + 1 if idx < len(modes) else 1

except KeyboardInterrupt:
    print("Arret manuel.")
finally:
    if process and process.poll() is None:
        process.terminate()
    pygame.quit()
    print("Fin de l’interaction.")
