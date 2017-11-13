import sys
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
YELLOW = (255, 255, 50)

TEXT_COLOR = BLACK
SCREEN_COLOR = WHITE

pygame.font.init()
mmt_menu_font = pygame.font.SysFont('Verdana', 30)
mmt_question_font = pygame.font.SysFont('Verdana', 90)
mmt_highlight_font = pygame.font.SysFont('Verdana', 250)

clock = pygame.time.Clock()

mmt = []


def create_multiplication_matrix():
    mmt.clear()
    for i in range(2, 10):
        for j in range(2, 10):
            mmt.append((i, j))
    random.shuffle(mmt)

    #for i in mmt:
    #    print(i)


def highlight_result(res, correct):
    if correct:
        screen.fill(GREEN)
        pygame.mixer.music.load('correct.mp3')
    else:
        screen.fill(RED)
        pygame.mixer.music.load('error.mp3')
    highlight_surface = mmt_highlight_font.render(str(res), False, TEXT_COLOR)
    screen.blit(highlight_surface, (300, 100))

    pygame.display.flip()
    pygame.mixer.music.play(0)
    pygame.time.wait(2000)
    pygame.event.get()


pygame.init()
size = width, height = 900, 600
screen = pygame.display.set_mode(size)
# mode = 1 == menu mode
# mode = 2 == game mode
mode = 1
mmt_index = 0
answer = ''
good_answers = 0
bad_answers = 0
tick_start = 0
round_tick_start = 0
result = ''


def validate(a, b, ga, ba):
    if len(answer)> 0:
        if a * b == int(answer):
            # answer is correct
            ga += 1
            highlight_result(a * b, True)
        else:
            # answer is wrong
            ba += 1
            mmt.append((a, b))
            highlight_result(a * b, False)
    else:
        ba += 1
        mmt.append((a, b))
        highlight_result(a * b, False)

    return ba, ga


while True:
    clock.tick(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                sys.exit()
            if mode == 3 and event.key == pygame.K_1:
                mode = 1
            if mode == 1 and event.key == pygame.K_SPACE:
                good_answers = 0
                bad_answers = 0
                result = ''
                create_multiplication_matrix()

                tick_start = pygame.time.get_ticks()
                round_tick_start = pygame.time.get_ticks()
                mode = 2
            if mode == 2:
                if event.key in range(pygame.K_0, pygame.K_9 + 1) or event.key in range(pygame.K_KP0, pygame.K_KP9 + 1):
                    answer += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    answer = answer[:-1]
                elif (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and len(answer) > 0:
                    a, b = mmt[mmt_index]
                    bad_answers, good_answers = validate(a, b, good_answers, bad_answers)
                    answer = ''
                    mmt_index += 1
                    if mmt_index == len(mmt):
                        # end of matrix - display result
                        mode = 3
                        result = str(good_answers) + ' correct and ' + str(bad_answers) + ' incorrect answers in ' \
                                 + str(int((pygame.time.get_ticks() - tick_start)/1000)) + ' secs, hit 1'

                    round_tick_start = pygame.time.get_ticks()

    screen.fill(SCREEN_COLOR)

    if mode == 1:
        # display menu
        menu_surface = mmt_menu_font.render('Hit Q for exit, Space to start', False, TEXT_COLOR)
        screen.blit(menu_surface, (200, 200))
    elif mode == 2:
        # play the game
        a, b = mmt[mmt_index]
        round_tick = pygame.time.get_ticks() - round_tick_start
        question_surface = mmt_question_font.render(str(a) +' x ' + str(b), False, TEXT_COLOR)
        answer_surface = mmt_question_font.render(answer, False, TEXT_COLOR)
        good_answer_surface = mmt_question_font.render(str(good_answers), False, GREEN)
        bad_answer_surface = mmt_question_font.render(str(bad_answers), False, RED)
        timer_surface = mmt_menu_font.render(str(int(pygame.time.get_ticks()/1000)), False, TEXT_COLOR)
        round_timer_surface = mmt_menu_font.render(str(round_tick/1000), False, TEXT_COLOR)
        screen.blit(question_surface, (300, 150))
        screen.blit(answer_surface, (365, 350))
        screen.blit(good_answer_surface, (100, 50))
        screen.blit(bad_answer_surface, (650, 50))
        screen.blit(timer_surface, (50, 550))
        screen.blit(round_timer_surface, (650, 550))

        color = (int(round_tick/20), 255-int(round_tick/20), 0)
        pygame.draw.rect(screen, color, (100+ int(round_tick/10), 550, 500-int(round_tick/10), 50))

        if round_tick_start <= pygame.time.get_ticks() - 5000:

            bad_answers, good_answers = validate(a, b, good_answers, bad_answers)

            answer = ''
            mmt_index += 1
            round_tick_start = pygame.time.get_ticks()
            if mmt_index == len(mmt):
                # end of matrix - display result
                mode = 3

    elif mode == 3:
        # display result
        result_surface = mmt_menu_font.render(result, False, TEXT_COLOR)
        screen.blit(result_surface, (10, 200))

    pygame.display.flip()
