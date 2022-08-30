import pickle
# /clone -93 4 45 -168 5 108 -168 4 182 /clone -93 1 45 -168 5 108 -168 4 182
# instantiate
# 46
import neat

import os
import pygame
import playerContoller


class MmAI():


    def __init__(self,port,code,ip ="localhost",gens=100,size=5,maxmoves =10,debug=False,display=False):
        self.port = port  #
        self.ip = ip  #
        self.size = size  #
        self.gens = gens  #
        self.debug = debug
        self.display = display
        self.maxmoves = maxmoves
        self.code = code
        currentRot = 0
        moves = ['forward', 'back', 'left', 'right']
        self.mkplayers = []
        self.players = []
        self.runner = None
        self.gen = 0
        self.Time = 0
        knownedBlocks = ["Grass_Block"]
        self.offset = (-5, -1, 0)
        print("starting adding players...")
        for i in range(self.size + 1):
            if i == self.size:
                self.runner = playerContoller.createAI(self.ip, self.port, f"runner")
            else:
                player = playerContoller.createAI(self.ip, self.port, f"{i}test")
                self.players.append(player)
        print("done adding players waiting them to join...")
        while not self.players[self.size - 2].Whenjoined():
            1
        if self.display:
            self.runner.chat(f"/bossbar set minecraft:gen name \" est time:{round(self.esttime(self.gen), 3)}| time:{self.Time}\"")
            self.runner.chat(f"/bossbar set minecraft:gen max {self.gens}")
            self.runner.chat(f"/bossbar set minecraft:gen value 0")
        print("staring neat...")
        # print(players[0].getBlocks(5,(0,0,0)))

        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, 'ai.txt')
        self.run(config_path)

    def esttime(self, currntgen):
        return ((20 * self.size) * self.gens - currntgen) / 60

    def eval_genomes(self, genomes, config):

        self.ge = []
        self.fitnesses = []

        mkplayers = self.players

        self.gen += 1
        if self.display:
            self.runner.chat(f"/scoreboard objectives add genout dummy \"gen:{self.gen}\"")
            self.runner.chat(f"/bossbar add gen \"est time:0\"")
            for i in range(0, self.size):

                self.runner.chat(f"/effect give {str(i)}test glowing 99999 1")
                self.runner.chat(f"/scoreboard players set {str(i)}test genout 0")
            self.runner.chat(f"/scoreboard objectives modify genout displayname \"gen:{self.gen}\"")
        # runner.chat(f"/clear {str(i)}test")
        for i in range(0, self.size):
            self.runner.chat(f"/tp {str(i)}test @s")

        nets = []
        for genome_id, genome in genomes:
            self.ge.append(genome)
            genome.fitness = 0
            self.fitnesses.append(genome.fitness)
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            # print(genome)

        for i, player in enumerate(self.players):
            for f in range(self.maxmoves):

                # geting blocks in a 5 block radius
                blocks = player.getBlockIds(5, self.offset)
                blocknames = player.getBlockNames(5, self.offset)
                pos = player.pos()
                # test = player.getinventory()
                # print(nets[0].node_evals)
                # contorling player
                outputs = nets[i].activate(tuple(blocks) + pos)
                self.code(outputs,i,player,blocknames,self.runner,self.display,self.fitnesses,self.ge,self.debug)
        if self.display:
            self.runner.chat(
                f" best of gen:{self.gen} player{self.fitnesses.index(max(self.fitnesses))} with fit of {max(self.fitnesses)} others {self.fitnesses}")
            self.runner.chat(f"/bossbar set minecraft:gen name \" est time:{round(self.esttime(self.gen), 3)}\"")
            self.runner.chat(f"/bossbar set minecraft:gen value {self.gen}")



    def run(self,config_path):
        config = neat.config.Config(neat.genome.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                    config_path)
        pop = neat.Population(config)

        winner = pop.run(self.eval_genomes, self.gens)
        with open("winner.pkl", "wb") as f:
            pickle.dump(winner, f)
            f.close()
        print("done outputed file")
