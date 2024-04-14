import pygame
import cv2

if __name__ == "__main__":

    pygame.init()

    screen = pygame.display.set_mode((1300, 800))

    run = True

    video = cv2.VideoCapture("assets/SoundTracks/SFX/lalala.mp4")
    pygame.mixer.music.load("assets/SoundTracks/SFX/lalala.mp3")
    pygame.mixer.music.play(0)
    clock = pygame.time.Clock()
    

    while run:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

        pygame.draw.circle(screen, "red", (200 ,200), 50, 4)

        
        success, video_image = video.read()
        if success :
            video_surf = pygame.image.frombuffer(video_image.tobytes(), video_image.shape[1::-1], "BGR")
            screen.blit(video_surf, (screen.get_width()/2 - video_surf.get_width()/2, screen.get_height()/2 - video_surf.get_height()/2))
            clock.tick(video.get(cv2.CAP_PROP_FPS))
        else :
            clock.tick(60)
        pygame.display.flip()
    
    pygame.quit()