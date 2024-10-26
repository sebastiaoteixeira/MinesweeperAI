from client import human, ai
import viewer
import argparse

# Executa o jogo
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Minesweeper')
    parser.add_argument('--player', type=str, default='human', help='Player type')

    args = parser.parse_args()
    if args.player == 'human':
        viewer.loop(human())
    elif args.player == 'ai':
        viewer.ai_mode = True
        viewer.loop(ai())