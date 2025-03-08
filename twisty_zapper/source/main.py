from game import Game


def main():
    game = Game()
    restart = game.play()
    if restart:
        main()


if __name__ == '__main__':
    main()
