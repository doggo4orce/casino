from color import *
import card_data
import cmd_trig_data
import commands
import config
import baccarat_dealer_data
import baccarat_hand_data
import baccarat_history_data
import cmd_trig_data
import mudlog
import string_handling

"""Special Procedures for the Baccarat dealer:

   baccarat_dealer_history() <- display the history of the shoe
   baccarat_dealer_intro()   <- basic response to a greeting
   baccarat_syntax_parser()  <- handles all syntax associated with the baccarat game
   baccarat_dealing()        <- handles the baccarat game"""

def baccarat_dealer_history(mud, me, ch, command, argument, db):
  if not isinstance(me, baccarat_dealer_data.baccarat_dealer_data):
    mudlog.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return

  if command != "history":
    return

  b_win = f"{BRIGHT_RED}*{NORMAL}"
  b_8 = f"{BRIGHT_RED}8{NORMAL}"
  b_9 = f"{BRIGHT_RED}9{NORMAL}"

  p_win = f"{BRIGHT_BLUE}*{NORMAL}"
  p_8 = f"{BRIGHT_BLUE}8{NORMAL}"
  p_9 = f"{BRIGHT_BLUE}9{NORMAL}"

  tie = f"{BRIGHT_GREEN}T{NORMAL}"
  panda = f"{BRIGHT_MAGENTA}P{NORMAL}"
  dragon = f"{BRIGHT_CYAN}D{NORMAL}"

  out_str = "  EZ Baccarat".ljust(33) + "\r\n"

  out_str += f"{YELLOW}+--------------+".ljust(33) + f"{b_win} - banker win\r\n"
  out_str += f"{YELLOW}|{BKGD_YELLOW}{b_win}{p_win}{p_win}           {YELLOW}|".ljust(76) + f"{b_8} - banker win with natural 8\r\n"
  out_str += f"{YELLOW}|{tie}{b_win}            {YELLOW}|".ljust(60) + f"{b_9} - banker win with natural 9\r\n"
  out_str += f"{YELLOW}|{b_win}{FLASH}{dragon}            {YELLOW}|".ljust(64) + f"{p_8} - player win with natural 8\r\n"
  out_str += f"{YELLOW}|{BKGD_YELLOW}{b_8}{tie}            {YELLOW}|".ljust(65) + f"{p_9} - player win with natural 9\r\n"
  out_str += f"{YELLOW}|{BKGD_CYAN}{p_9}{b_win}            {YELLOW}|".ljust(65) + f"{tie} - tie\r\n"
  out_str += f"{YELLOW}|{FLASH}{panda}{BKGD_WHITE}{b_9}            {YELLOW}|".ljust(69) + f"{panda} - panda\r\n"
  out_str += f"{YELLOW}+--------------+{NORMAL}".ljust(37) + f"{dragon} - dragon\r\n\r\n"

  out_str += f"{BKGD_YELLOW} {NORMAL} - any 8 over 7\r\n"
  out_str += f"{BKGD_CYAN} {NORMAL} - three card 9 over 8\r\n"
  out_str += f"{BKGD_WHITE} {NORMAL} - natural 9 over 8\r\n"
  ch.write(out_str)

  return cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER

def baccarat_dealer_intro(mud, me, ch, command, argument, db):
  if not isinstance(me, baccarat_dealer_data.baccarat_dealer_data):
    logging.warning(f"Attempting to call inappropriate spec proc 'baccarat_dealer_intro' on npc {me}.")
    return
  if command == "say" and argument.lower() == "hi":
    commands.do_say(me, None, "Hey, wanna play some Baccarat?  Type 'baccarat' for more information.", None, mud, db)
    return

def baccarat_dealer_syntax_parser(mud, me, ch, command, argument, db):
  if not isinstance(me, baccarat_dealer_data.baccarat_dealer_data):
    logging.warning(f"Attempting to call inappropriate spec_proc 'baccarat_dealer_syntax_parser' on npc {me}.")
    return

  help_str  = "Baccarat Commands:\r\n"
  help_str += "  baccarat chips         - ask dealer for a set of chips\r\n"
  help_str += "  baccarat playing       - see who is playing the game\r\n"
  help_str += "  baccarat start         - start the game\r\n"
  help_str += "  baccarat simulate      - simulate a baccarat shoe (fast)\r\n"
  help_str += "  baccarat stop          - stop the game\r\n"
  help_str += "\r\n"
  help_str += "Gameplay Commands:\r\n"
  help_str += "  sit                    - sit down at the table (if there is room)\r\n"
  help_str += "  leave                  - stand up and leave the table\r\n"
  help_str += "  bet <player or banker> - bet a red chip on player or banker\r\n"

  if command == "bet":
    if me.bac_state not in [
      baccarat_dealer_state.BEGIN_SHOE,
      baccarat_dealer_state.SHUFFLE_SHOE,
      baccarat_dealer_state.FIRST_DRAW,
      baccarat_dealer_state.BURN_CARDS,
      baccarat_dealer_state.LAST_CALL_BETS,
      baccarat_dealer_state.NO_MORE_BETS]:  # <-- hasn't quite said no more bets
      ch.write("The dealer slaps you.\r\n")
      return cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER
    else:
      ch.write("You put a red chip down on the table.\r\n")
      return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
  elif command == "baccarat":
    if argument.lower() == "playing":
      if len(me.players) == 0:
        commands.do_say(me, None, f"Right now, we have nobody playing!", None, mud, db)
      else:
        names = [name.capitalize() for name in me.players]
        commands.do_say(me, None, f"Right now, we have {string_handling.oxford_comma(names)} playing.", None, mud, db)
    elif argument.lower() == "stop":
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.IDLE
    elif argument.lower() in ["start", "simulate"]:
      if me.bac_state != baccarat_dealer_data.baccarat_dealer_state.IDLE:
        ch.write("There is already a game in progress!\r\n")
        return spec_procs.prefix_command_trigger_messages.BLOCK_INTERPRETER
      ch.write("You signal to the dealer to start the next shoe.\r\n")

      mudlog.debug(f"{ch} signals to the dealer to start the next shoe.")
      mud.echo_around(ch, None, f"{ch} signals to the dealer to start the next shoe.\r\n")
      me.bac_paused = 10
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.BEGIN_SHOE
  
      if argument.lower() == "simulate":
        me.simulation_mode = True
    elif argument.lower() == "chips":
      ch.write("You ask the dealer for some chips to play with.\r\n")
      ch.write(f"{me} nods in your direction without comment.\r\n")
      mud.echo_around(ch, None, f"{me} nods in {ch}'s direction without comment.\r\n")

      for n in range(0, 5):
        red_chip = mud.load_obj('stockville[red_chip]')
        ch.inventory.insert(red_chip)

      ch.write(f"{me} gives you five red chips.")
      mud.echo_around(ch, None, f"{me} gives {ch} five red chips.")

    else:
      ch.write(help_str)
    return cmd_trig_data.prefix_cmd_trig_messages.BLOCK_INTERPRETER
  elif command == "bet":
    if argument.lower() in ["player", "banker"]:
      pass
    pass

def baccarat_dealing(mud, me, db):
  NUM_DECKS = 6

  panda_string = "{}P{}a{}n{}d{}a{}!{}".format(CYAN, DARK_GRAY, CYAN, DARK_GRAY, CYAN, DARK_GRAY, NORMAL)
  dragon_string = "{}D{}r{}a{}g{}o{}n{}!{}".format(CYAN, GREEN, CYAN, GREEN, CYAN, GREEN, CYAN, NORMAL)

  mudlog.debug(f"{me}.bac_state is {me.bac_state.name}")
  # mudlog.debug(f"{me}.bac_paused is {me.bac_paused}")

  if me.bac_state == baccarat_dealer_data.baccarat_dealer_state.IDLE:
    return

  if me.bac_paused > 0 and not me.simulation_mode:
    me.bac_paused -= 1
    return

  if not isinstance(me, baccarat_dealer_data.baccarat_dealer_data):
    logging.warning(f"{me} attempting to call 'baccarat_dealing' but is not a baccarat dealer")
    return

  if me.bac_state == baccarat_dealer_data.baccarat_dealer_state.BEGIN_SHOE:
    me.give_french_decks(NUM_DECKS)
    mud.echo_around(me, None, f"{me} assembles a new shoe consisting of {NUM_DECKS} deck{'s' if NUM_DECKS > 1 else ' '}.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.SHUFFLE_SHOE
    pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.SHUFFLE_SHOE:
    me.shuffle()
    mud.echo_around(me, None, f"{me} shuffles the shoe.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.FIRST_DRAW
    pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.FIRST_DRAW:
    first_card = me.draw()
    me.initial_card_val = baccarat_hand_data.baccarat_hand_data.card_value(first_card)
    mud.echo_around(me, None, "{} draws the first card, which is {} {}.\r\n".format(
      me, string_handling.ana(card_data.card_rank(first_card.rank).name), first_card))
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.BURN_CARDS
    pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.BURN_CARDS:
    for j in range(0, me.initial_card_val):
      me.draw()
    mud.echo_around(me, None, f"{me} burns {me.initial_card_val} card{'s' if me.initial_card_val > 1 else ''}.\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.LAST_CALL_BETS
    pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.LAST_CALL_BETS:
    commands.do_say(me, None, f"Last call, any more bets?", None, mud, db)
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.NO_MORE_BETS
    pause = 120
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.NO_MORE_BETS:
    mud.echo_around(me, None, f"{me} gestures and says, 'No more bets.'\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.PLAYER_FIRST
    pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.PLAYER_FIRST:
    if me.shoe_length() < 6:
      commands.do_say(me, None, "Ladies and gentlemen, that was our final hand.  Thanks for playing!", None, mud, db)
      mud.echo_around(me, None, "Player wins: {}{}{} (including pandas)\r\nBanker wins: {}{}{}\r\nTies: {}{}{}\r\nPandas: {}{}{}\r\nDragons: {}{}{}\r\n".format(
        BLUE, me.shoe.count_reports(baccarat_history_data.history_entry.PLAYER_WIN) + me.shoe.count_reports(history_entry.PANDA), NORMAL,
        RED, me.shoe.count_reports(baccarat_history_data.history_entry.BANKER_WIN), NORMAL,
        GREEN, me.shoe.count_reports(baccarat_history_data.history_entry.TIE), NORMAL,
        MAGENTA, me.shoe.count_reports(baccarat_history_data.history_entry.PANDA), NORMAL,
        CYAN, me.shoe.count_reports(baccarat_history_data.history_entry.DRAGON), NORMAL))
      mud.echo_around(me, None, "3-card 9/8's: {}{}{}\r\nNatural 9/8's: {}{}{}\r\nAny 8/7's: {}{}{}\r\n".format(
        YELLOW, me.shoe.count_extras(baccarat_history_data.extra_side_bet.THREE_CARD_9_8), NORMAL,
        YELLOW, me.shoe.count_extras(baccarat_history_data.baccarat_history_data.extra_side_bet.NATURAL_9_8), NORMAL,
        YELLOW, me.shoe.count_extras(baccarat_history_data.extra_side_bet.ANY_8_7), NORMAL
        ))
      me.clear_shoe()
      me.bac_state = baccarat_dealer_state.IDLE
      me.bac_paused = 0
      me.simulation_mode = False
      return
    me.clear_baccarat_hand()
    card = me.draw()
    me.deal(card, 'player')
    mud.echo_around(me, None, f"{me} deals {card} to the player.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.BANKER_FIRST
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.BANKER_FIRST:
    card = me.draw()
    me.deal(card, 'banker')
    mud.echo_around(me, None, f"{me} deals {card} to the banker.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.PLAYER_SECOND
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.PLAYER_SECOND:
    card = me.draw()
    me.deal(card, 'player')
    mud.echo_around(me, None, f"{me} deals {card} to the player.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.BANKER_SECOND
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.BANKER_SECOND:
    card = me.draw()
    me.deal(card, 'banker')
    mud.echo_around(me, None, f"{me} deals {card} to the banker.\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.SHOW_INITIAL
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.SHOW_INITIAL:
    #mud.echo_around(me, None, me.hand.display() + "\n\n")
    commands.do_say(me, None, f"Player shows {me.player_score()}. Banker shows {me.banker_score()}.", None, mud, db)
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.CHECK_NATURAL
    pause = 60
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.CHECK_NATURAL:
    if me.player_natural():
      commands.do_say(me, None, f"Player shows natural {me.player_score()}.  No more draws.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.REPORT_WINNER
      pause = 30
    elif me.banker_natural():
      commands.do_say(me, None, f"Banker shows natural {me.banker_score()}.  No more draws.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.REPORT_WINNER
      pause = 30
    else:
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.CHECK_PLAYER
      pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.CHECK_PLAYER:
    if me.player_third():
      commands.do_say(me, None, "Card for player.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.DEAL_PLAYER_THIRD
    else:
      commands.do_say(me, None, "Player stands.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.CHECK_BANKER
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.DEAL_PLAYER_THIRD:
    player_third = me.draw()
    me.deal(player_third, 'player')
    mud.echo_around(me, None, "{} deals {} {} to the player.\r\n".format(
      me, string_handling.ana(card_data.card_rank(player_third.rank).name), player_third))
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.UPDATE_PLAYER_THIRD
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.UPDATE_PLAYER_THIRD:
    #mud.echo_around(me, None, "\n" + me.hand.display() + "\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.CHECK_BANKER
    pause = 60
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.CHECK_BANKER:
    if me.banker_third():
      commands.do_say(me, None, "Card for banker.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.DEAL_BANKER_THIRD
      pause = 10
    else:
      commands.do_say(me, None, "Banker stands.", None, mud, db)
      me.bac_state = baccarat_dealer_data.baccarat_dealer_state.REPORT_WINNER
      pause = 30
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.DEAL_BANKER_THIRD:
    banker_third = me.deal_next_card('banker')
    mud.echo_around(me, None, "{} deals {} {} to the banker.\r\n".format(
      me, string_handling.ana(card_data.card_rank(banker_third.rank).name), banker_third))
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.UPDATE_BANKER_THIRD
    pause = 10
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.UPDATE_BANKER_THIRD:
    #mud.echo_around(me, None, "\n" + me.hand.display() + "\r\n")
    me.bac_state = baccarat_dealer_data.baccarat_dealer_state.REPORT_WINNER
    pause = 60
  elif me.bac_state == baccarat_dealer_data.baccarat_dealer_state.REPORT_WINNER:
    if me.panda():
      commands.do_say(me, None, panda_string, None, mud, db)
      me.report_history(baccarat_history_data.history_entry.PANDA)
    elif me.dragon():
      commands.do_say(me, None, dragon_string, None, mud, db)
      me.report_history(baccarat_history_data.history_entry.DRAGON)
    elif me.player_score() > me.banker_score():
      commands.do_say(me, None, f"Player wins {me.player_score()} over {me.banker_score()}.", None, mud, db)
      me.report_history(baccarat_history_data.history_entry.PLAYER_WIN)
    elif me.player_score() < me.banker_score():
      commands.do_say(me, None, f"Banker wins {me.banker_score()} over {me.player_score()}.", None, mud, db)
      me.report_history(baccarat_history_data.history_entry.BANKER_WIN)
    else:
      commands.do_say(me, None, f"Player and banker tie!", None, mud, db)
      me.report_history(history_entry.TIE)
    # Check Michael's Side Bets
    if me.three_card_9_8():
      me.report_extra(extra_side_bet.THREE_CARD_9_8)
    if me.natural_9_8():
      me.report_extra(extra_side_bet.NATURAL_9_8)
    if me.any_8_7():
      me.report_extra(extra_side_bet.ANY_8_7)
    me.clear_baccarat_hand()
    me.bac_state = baccarat_dealer_state.CLEAR_CARDS
    pause = 60
  elif me.bac_state == baccarat_dealer_state.CLEAR_CARDS:
    mud.echo_around(me, None, f"{me} clears the cards from the table.\n")
    me.bac_state = baccarat_dealer_state.LAST_CALL_BETS
    pause = 120

  if pause != 0 and not me.simulation_mode:
    me.bac_paused = pause
 
  return
  