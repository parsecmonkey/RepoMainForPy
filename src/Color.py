# 色

BLACK          = '\033[30m' # (文字)黒
RED            = '\033[31m' # (文字)赤
GREEN          = '\033[32m' # (文字)緑
YELLOW         = '\033[33m' # (文字)黄
BLUE           = '\033[34m' # (文字)青
MAGENTA        = '\033[35m' # (文字)マゼンタ
CYAN           = '\033[36m' # (文字)シアン
WHITE          = '\033[37m' # (文字)白
COLOR_DEFAULT  = '\033[39m' # 文字色をデフォルトに戻す
BOLD           = '\033[1m'  # 太字
UNDERLINE      = '\033[4m'  # 下線
INVISIBLE      = '\033[08m' # 不可視
REVERCE        = '\033[07m' # 文字色と背景色を反転
BG_BLACK       = '\033[40m' # (背景)黒
BG_RED         = '\033[41m' # (背景)赤
BG_GREEN       = '\033[42m' # (背景)緑
BG_YELLOW      = '\033[43m' # (背景)黄
BG_BLUE        = '\033[44m' # (背景)青
BG_MAGENTA     = '\033[45m' # (背景)マゼンタ
BG_CYAN        = '\033[46m' # (背景)シアン
BG_WHITE       = '\033[47m' # (背景)白
BG_DEFAULT     = '\033[49m' # 背景色をデフォルトに戻す
RESET          = '\033[0m'  # 全てリセット

if __name__ == "__main__":
    print(f'黒:{BLACK}●ABC{RESET}')
    print(f'赤:{RED}●ABC{RESET}')
    print(f'緑:{GREEN}●ABC{RESET}')
    print(f'黄:{YELLOW}●ABC{RESET}')
    print(f'青:{BLUE}●ABC{RESET}')
    print(f'マゼンタ:{MAGENTA}●ABC{RESET}')
    print(f'シアン:{CYAN}●ABC{RESET}')
    print(f'白:{WHITE}●ABC{RESET}')
    print(f'下線:{UNDERLINE}●ABC{RESET}')
    print(f'太字:{BOLD}●ABC{RESET}')
    print(f'不可視:{INVISIBLE}●ABC{RESET}')
    print(f'反転:{REVERCE}●ABC{RESET}')
    print(f'背景黒:{BG_BLACK}●ABC{RESET}')
    print(f'背景赤:{BG_RED}●ABC{RESET}')
    print(f'背景緑:{BG_GREEN}●ABC{RESET}')
    print(f'背景黄:{BG_YELLOW}●ABC{RESET}')
    print(f'背景青:{BG_BLUE}●ABC{RESET}')
    print(f'背景マゼンタ:{BG_MAGENTA}●ABC{RESET}')
    print(f'背景シアン:{BG_CYAN}●ABC{RESET}')
    print(f'背景白:{BG_WHITE}●ABC{RESET}')
    print(f'文字赤+背景緑:{RED}{BG_GREEN}●ABC{RESET}') # 文字色と背景色を変える