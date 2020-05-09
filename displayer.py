from utils import *
import display_utils
import tkinter
import time
import copy
import os

class GameDisplayer:
    def __init__(self):
        pass
    
    def InitDisplayer(self,runner):
        pass
            
    def ExcuteMove(self,i,move,game_state):
        pass

    def TimeOutWarning(self,runner,id):
        pass

    def StartRound(self,game_state):
        pass
    
    def EndRound(self,game_state):
        pass
    
    def EndGame(self,game_state):
        pass

class GUIGameDisplayer(GameDisplayer):
    def __init__(self,delay = 0.1):
        self.delay = delay

    def InitDisplayer(self,runner):
        self.root = tkinter.Tk()
        self.center_token = True
        self.root.title("AZUL assignment ------ COMP90054 AI Planning for Autononmy")

        self.root.tk.call('wm', 'iconphoto', self.root._w, tkinter.PhotoImage(file='resources/azul_bpj_icon.gif'))
        self.root.geometry("1300x700")
        # self.root.resizable(width=False, height=False)

        self.tile_images = []
        self.tile_images.append(tkinter.PhotoImage(file="resources/blue_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/yellow_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/red_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/black_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/white_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/start_tile_mini.gif"))
        self.tile_images.append(tkinter.PhotoImage(file="resources/penalty_tile_mini.gif"))
        
        self.player_borad_img = tkinter.PhotoImage(file="resources/player_board_mini.gif")
        self.m_img = tkinter.PhotoImage(file="resources/multiplication_mini.gif")


        #factory
        self.fb_frame = tkinter.Frame(self.root)
        self.fb_frame.grid(row=0,column=0,sticky=tkinter.W+tkinter.E)

        self.board_factories = []
        self.ft_num = []
        for i in range(5):
            self.ft_num.append([tkinter.StringVar() for _ in range(5)])
        self.ft_num.append([tkinter.StringVar() for _ in range(6)])
        for row in self.ft_num:
            for var in row:
                var.set("0") 
        
        for i in range(5):
            factory = display_utils.BoardFactory(i)
            factory.factory_displayer = tkinter.Frame(self.fb_frame,highlightbackground="black", highlightcolor="black", highlightthickness=3, borderwidth=2)
            factory.factory_displayer.grid(row=i,column=0)
            #factory.factory_displayer.grid_propagate(False)
            self._GenerateFactory(factory,i,5)
            self.board_factories.append(factory)
        self.cf_board = display_utils.BoardFactory(6)
        self.cf_board.factory_displayer = tkinter.Frame(self.fb_frame,highlightbackground="black", highlightcolor="black", highlightthickness=3)
        self.cf_board.factory_displayer.grid(row=5,column=0)
        self._GenerateFactory(self.cf_board,5,6)

        
        #player board
        self.pb_frame = tkinter.Frame(self.root)
        self.pb_frame.grid(row=0,column=1,sticky=tkinter.W+tkinter.E)

        self.player_board = []
        # assert(len(player_list) == 2)
        for i in range(2):
            name=tkinter.StringVar()
            name.set("Player ("+str(i)+"): "+str(runner.players_namelist[i])+"")
            pb1 = display_utils.PlayerBoard(i,tkinter.Canvas(self.pb_frame, width=405, height=265),tkinter.Entry(self.pb_frame, textvariable=name ,width=40))
            pb1.naming.grid(row=i*2,column=0)
            pb1.display_board.grid(row=i*2+1, column=0)
            pb1.display_board.create_image(0,0, anchor=tkinter.NW, image=self.player_borad_img) 

            self.player_board.append(pb1)
            

        #scoreboard
        self.sb_frame = tkinter.Frame(self.root)
        self.sb_frame.grid(row=0, column=2, sticky=tkinter.N+tkinter.E)

        self.scrollbar = tkinter.Scrollbar(self.sb_frame, orient=tkinter.VERTICAL)

        self.move_box=tkinter.Listbox(self.sb_frame,name="moves:", height=37, width=88, selectmode="single", borderwidth=4,yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.move_box.yview,troughcolor="white",bg="white")
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.move_box.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)   
        # self.move_box.configure(exportselection=False)
        # self.move_box.configure(state=tkinter.DISABLED)

        # self.move_box.grid(row=0, column=3, rowspan=3, sticky=tkinter.N+tkinter.E)
        
        #self.fb_frame.grid_propagate(0)
        #self.root.grid_propagate(0)

        self.game_state_history=[]
        self.round_num = 0

    def _InsertState(self,text,game_state):
        text = text.replace("\n ","")
        self.game_state_history.append(copy.deepcopy(game_state))
        self.move_box.insert(tkinter.END,text)
        self.move_box.see(tkinter.END)
        self.move_box.selection_clear(0, last=None) 

    def _GenerateFactory(self,parent,index,size):
        
        for j in range(size):
            tf = tkinter.Frame(parent.factory_displayer,highlightbackground="grey", highlightcolor="grey", highlightthickness=2,borderwidth=2, width=39, height = 80)
            tf.grid(row=0,column=j)
            td = tkinter.Canvas(tf, width=35, height=35)
            td.create_image(0,0, anchor=tkinter.NW, image=self.tile_images[j]) 
            td.grid(row=0,column=0)
            m = tkinter.Canvas(tf, width=35, height=15)
            m.create_image(10,0, anchor=tkinter.NW, image=self.m_img) 
            m.grid(row=1,column=0)
            num = tkinter.Label(tf,textvariable=self.ft_num[index][j],borderwidth=4,relief=tkinter.SUNKEN)
            num.grid(row=2,column=0)

    def _UpdateFactory(self,game_state):
        inuses = [False] * 6

        #color
        for i in range(5):
            # tile num by factory
            for j in range(5):
                self.ft_num[j][i].set(str(game_state.factories[j].tiles[i]))
                if game_state.factories[j].tiles[i] > 0:
                    inuses[j] = True
            self.ft_num[5][i].set(str(game_state.centre_pool.tiles[i]))
            if game_state.centre_pool.tiles[i] > 0:
                inuses[-1] = True

        if game_state.next_first_player!=-1:
            self.ft_num[5][5].set("0")
        else:
            self.ft_num[5][5].set("1")
        
        for i,inuse in enumerate(inuses[:-1]):
            if inuse:
                self.board_factories[i].factory_displayer.config(highlightbackground="red")
            else:
                self.board_factories[i].factory_displayer.config(highlightbackground="black")

        if inuses[-1]:
            self.cf_board.factory_displayer.config(highlightbackground="red")
        else:
            self.cf_board.factory_displayer.config(highlightbackground="black")

    def _UpdateLine(self,tile_num,play_board,line_id,tile_id):

        for i,tile in enumerate(play_board.playing_board[line_id].tiles):
            if not tile.empty:
                play_board.display_board.delete(tile.content)
                tile.empty = True
            if i < tile_num:
                tile.empty = False
                tile.content = play_board.display_board.create_image(tile.x,tile.y, anchor=tkinter.NW, image=self.tile_images[tile_id])
                play_board.display_board.update()
    
    def _UpdateScoringLine(self,play_board,index,cells):
        tt=0
        cc = 17 #circle center
        cs = 10 #circle size

        for x,(t,c) in enumerate(zip(play_board.scoring_board[index].tiles,cells)):
            if not t.empty:
                for content in t.content:
                    play_board.display_board.delete(content)
                t.empty = True

            if c != 0 and t.empty:
                t.empty = False
                tt = (5+x-index +1 ) % 5 - 1
                if tt < 0:
                    tt = tt + 5
                t.content = [
                    play_board.display_board.create_image(t.x,t.y, anchor=tkinter.NW, image=self.tile_images[tt]),
                    play_board.display_board.create_oval(t.x+cc-cs,t.y+cc-cs,t.x+cc+cs,t.y+cc+cs, fill = "lawn green")
                ]
                play_board.display_board.update()
    
    def _DisplayState(self,game_state):

        # update player board one by one
        for _,(ps,pb) in enumerate(zip(game_state.players,self.player_board)):

            # update playing board 
            for line_num in range(ps.GRID_SIZE):
                self._UpdateLine(ps.lines_number[line_num],pb,line_num,ps.lines_tile[line_num])
            
            # update floor line
            if game_state.next_first_player != -1:
                self._UpdateLine(1,pb,5,5)
            else:
                 self._UpdateLine(0,pb,5,5)

            penalty = 0
            for i in ps.floor:
                if i == 1:
                    penalty = penalty + 1
            self._UpdateLine(penalty,pb,5,6)

            # update the scoring board

            for i in range(5):
                cells = [ps.grid_state[i][j] for j in range(5)]
                self._UpdateScoringLine(pb,i,cells)
        
        self._UpdateFactory(game_state)

    def StartRound(self,game_state):
        self._DisplayState(game_state)
        self.round_num = self.round_num +1
        self._InsertState("~~~~~~~~~~~~~~~Start of round: "+str(self.round_num)+"~~~~~~~~~~~~~~~",game_state)
        time.sleep(self.delay)

    def ExcuteMove(self,player_id,move, game_state):

        movement = move[2]
        #print(movement.num_to_pattern_line)
        if movement.num_to_pattern_line > 0:
            self._UpdateLine(movement.num_to_pattern_line,self.player_board[player_id],movement.pattern_line_dest,movement.tile_type)

        if move[0] == 2 and self.center_token:
            self.center_token = False
            self._UpdateLine(1,self.player_board[player_id],5,5)

        if movement.num_to_floor_line > 0:
            self._UpdateLine(movement.num_to_floor_line,self.player_board[player_id],5,6)

        self._InsertState(MoveToString(player_id,move),game_state)

        self._UpdateFactory(game_state)
        
        time.sleep(self.delay)

    def TimeOutWarning(self,runner,id):
        self._InsertState("Player {} time out, {} out of {}".format(id, runner.warnings[id],runner.warning_limit),runner.game_state)
        if id == 0:
            self.move_box.itemconfig(tkinter.END, {'bg':'red','fg':'blue'})
        else:
            self.move_box.itemconfig(tkinter.END, {'bg':'blue','fg':'yellow'})
        pass
    
    def EndRound(self,game_state):
        self.center_token = True
        self._DisplayState(game_state)
        self._InsertState("--------------End of round-------------",game_state)
        for i,plr_state in enumerate(game_state.players):
            self._InsertState("Current score for Player {}: {}".format(i,plr_state.score),game_state)
        time.sleep(self.delay)
        pass
    
    def EndGame(self,game_state):
        self._InsertState("--------------End of game-------------",game_state)
        for i,plr_state in enumerate(game_state.players):
            self._InsertState("Final score with bonus for Player {}: {}".format(i,plr_state.score),game_state)
        
        # text display for multiple games
        # result = "Final score with bonus for"
        # for i,plr_state in enumerate(game_state.players):
        #     result = result + " Player "+str(i)+": "+str(plr_state.score)+"; "
        # print(result+"\n")

        self.focus = None
        def OnHistorySelect(event):
            w = event.widget
            self.focus = int(w.curselection()[0])
            if self.focus < len(self.game_state_history):
                self._DisplayState(self.game_state_history[self.focus])
        def OnHistoryMove(event):
            if event.keysym == "Up":
                if self.focus>0:
                    self.move_box.select_clear(self.focus)
                    self.focus -=1
                    self.move_box.select_set(self.focus)
                    if self.focus < len(self.game_state_history):
                        self._DisplayState(self.game_state_history[self.focus])
            if event.keysym == "Down":
                if self.focus<len(self.game_state_history)-1:
                    self.move_box.select_clear(self.focus)
                    self.focus +=1
                    self.move_box.select_set(self.focus)
                    self._DisplayState(self.game_state_history[self.focus])


        self.move_box.bind('<<ListboxSelect>>', OnHistorySelect)
        self.move_box.bind('<Up>', OnHistoryMove)
        self.move_box.bind('<Down>', OnHistoryMove)


    
        self.root.mainloop()
        pass    



class TextGameDisplayer(GameDisplayer):
    def __init__(self):
        print ("--------------------------------------------------------------------")
        return

    def InitDisplayer(self,runner):
        pass

    def StartRound(self,game_state):
        pass    

    def ExcuteMove(self,i,move, game_state):
        plr_state = game_state.players[i]
        print("\nPlayer {} has chosen the following move:".format(i))
        print(MoveToString(i, move))
        print("\n")
        
        print("The new player state is:")
        print(PlayerToString(i, plr_state))
        print ("--------------------------------------------------------------------")
        
    def TimeOutWarning(self,runner,id):
        print ( "Player {} Time Out, {} out of {}.".format(id,runner.warnings[i],runner.warning_limit))
    
    def EndRound(self,state):
        print("ROUND HAS ENDED")
        print ("--------------------------------------------------------------------")

    def EndGame(self,game_state):
        print("GAME HAS ENDED")
        print ("--------------------------------------------------------------------")
        for plr_state in game_state.players:
            print ("Score for Player {}: {}".format(plr_state.id,plr_state.score))



class RecordGameDisplayer(GameDisplayer):
    def __init__(self):
        self.game_states = []
        pass
    
    def InitDisplayer(self,runner):
        pass
            
    def ExcuteMove(self,i,move,game_state):
        self.game_states.append((i,copy.deepcopy(game_state)))
        pass

    def TimeOutWarning(self,runner,id):
        pass

    def StartRound(self,game_state):
        self.game_states.append((-1,copy.deepcopy(game_state)))
        pass
    
    def EndRound(self,game_state):
        pass
    
    def EndGame(self,game_state):
        pass