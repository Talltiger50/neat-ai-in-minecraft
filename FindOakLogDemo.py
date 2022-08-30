import mmAi


def makePos(num):
    if 0 < num:
        return num
    return -1 * num
def code(outputs,currntplayer,player,blocknames,runner,display,fitnesses,ge,debug):
    i=currntplayer
    if outputs[0] > 0:
        player.move('forward', makePos(outputs[1]))
    if outputs[0] < 0:
        player.move('back', makePos(outputs[1]))
    if outputs[2] > 0:
        player.move('left', makePos(outputs[3]))
    if outputs[2] < 0:
        player.move('right', makePos(outputs[3]))
    if outputs[4] > 0.5:
        player.move("jump", makePos(outputs[5]))

    # reward system

    istherealog = "Oak Log" in blocknames
    if istherealog:
        ge[i].fitness += 10
        fitnesses[i] += 10
        if debug:
            print(i, "+10")
        if display:
            runner.chat(f"/scoreboard players add {str(i)}test genout 10")
    else:
        ge[i].fitness -= 1
        fitnesses[i] -= 1
        if debug:
            print(i, "-10")
        if display:
            runner.chat(f"/scoreboard players remove {str(i)}test genout 1")
    if debug:
        print(blocknames, "Oak Log" in blocknames)




main.MmAI(64893,code,display=True)