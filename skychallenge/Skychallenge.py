import discord
import datetime
import operator
#from discord.ext import commands
from redbot.core import commands, checks

bot = commands.Bot
BaseCog = getattr(commands, "Cog", object)

class challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot      
        
        @commands.command()
        async def createChallenge(ctx, answer, num, first, second, third, base):
            try:
                sender = str(ctx.message.author)  # makes it easier to get user in the future. In format of username#numbers
                ID = str(ctx.message.author.id)
                channel = str(ctx.message.channel) # channel message was sent from, used for checking if it was sent from a direct message
                if channel == ("Direct Message with %s" % (sender)):  # if the command was sent from a DM:
                    if ID == 'Authorized user ID here':
                        await ctx.send("You're an authorized user!")
                        # initialization of challenge files: The answer file, the point framework file, and the completed list file
                        challenge_file = open("Challenge_"+ str(num) + '.txt', "w+") # answer file
                        challenge_file.write(str(answer))
                        challenge_file.close()
                        challenge_point = open("Challenge_" + str(num)+ "_pointBase.txt", 'a+') # point framework file
                        challenge_point.write(str(first) + '\n' + str(second) + '\n' + str(third) + '\n' + str(base))
                        challenge_point.close()
                        challenge_complete = open("Challenge_" + str(num) + '_' +'completed.txt', 'w+' ) # completed list file
                        challenge_complete.close()
                        await ctx.send("Challenge created!")
                    else:
                        await ctx.send("You're not authorized to use this command!")
                else:
                    await ctx.send("This isn't a dm!")
            except:
                await ctx.send("An error occured. Please check your command to ensure correctness.")
        
        @commands.command()
        async def ch(ctx, num, answer):  # This is the command for submitting a flag for points, num is the challenge number, answer is the flag
            try:
                sender = str(ctx.message.author)  # makes it easier to get user in the future. In format of username#numbers
                ID = str(ctx.message.author.id)
                channel = str(ctx.message.channel) # channel message was sent from, used for checking if it was sent from a direct message
                if channel == ("Direct Message with %s" % (sender)):  # if the command was sent from a DM:
                    challenge_file = open('Challenge_' + str(num) + '.txt', 'r+')  # open the file that contains the correct flag for the given challenge
                    challenge = challenge_file.readlines() # read the file
                    flag = challenge[0]
                    flag = flag.strip('\n')
                    if answer == challenge[0]: # if the given answer is the same as the challenge answer:
                        challenge_file.close() # close the file
                        completed_list = open("Challenge_" + str(num) + '_' +'completed.txt', 'r+' ) # open the list of people who already completed that challenge
                        completed = completed_list.readlines() 
                        completeBool = False # set the assumption to be they haven't completed the challenge
                        for completion in completed: # iterate over the 
                            completion = completion.strip('\n')
                            if ID == completion: # if the author of the message is in the file
                                completeBool = True # set the completion var to true
                                await ctx.send("You've already completed this challenge!") # notify user
                            else: # if the author is not in the individual line
                                continue # keep going
                        completed_list.close() # close the file now that the program is done with ti
        
                        if completeBool == False: # If the user has not completed the challenge yet:
                            await ctx.send("Correct! Adding points...") # tell them the answer is correct
                            completed_list = open("Challenge_" + str(num) + '_' +'completed.txt', 'a+' ) # open the completed challenge files
                            completed_list.write(ID + '\n') # add the sender's name
                            completed_list.close() # close file
                            
                            # code to add points
                            point_File = open('Points.txt', "r") # open the global points file
                            # format should be: ID,points
                            points_List = [] # a list of all people's point scores that were in the file
                            for line in point_File: # for each line in the point file
                                line = line.strip('\n')
                                points_List.append(line) # add each line to the list
                            
                            point_File.close() 
        
                            found = False
                            point_loc = 0
                            for item in points_List: # find the sender of the flag in the list
                                user_points = item.find(ID) # the .find function returns the index of the given string. If the string is not found, it returns -1
                                if user_points != -1: # if the sender's name is found in the item:
                                    found = True # call found true
                                    point_place = item.find(',') # finds where the split between name and points are
                                    points = item[(point_place + 1):] # var is all chars after the comma
                                    points = int(points) # turn the string number into an integer to be manipulated
                                    guide = open("Challenge_" + str(num)+ "_pointBase.txt", 'r') # point framework file
                                    frame = [] # list that hold the point framework for use
                                    # Point file is formatted as the total number of points awarded for first, second, and third place followed by the base point total
                                    for line in guide: # putting the point framework from the file into the list
                                        line = line.strip('\n') # strip off EOL character
                                        frame.append(line) # add to list
                                    guide.close() # close point framework file. Leaving files open is bad
                                    if len(completed) == 0: # if the file with a list of users who already completed is empty...
                                        await ctx.send("You answered first! +" + str(frame[0] + " points!")) # tell them they answer first at their first place point bonus
                                        points += int(frame[0]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        # writing the point total back in the file
                                        points_List[point_loc] = (ID + "," + str(points)) # overwriting the item in the list where the old point total is with the new point total
                                        point_File = open('Points.txt', "w") # open the global points file in write mode
                                        for score in points_List: # essentially overwritting the entire file with the scores over again. Jank I know
                                            point_File.write(score + '\n')
                                        point_File.close()
                                
                                    elif len(completed) == 1: # if the file with a list of users who already completed is only one...
                                        await ctx.send("You answered Second! +" + str(frame[1] + " points!"))
                                        points += int(frame[1]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        # writing the point total back in the file
                                        points_List[point_loc] = (ID + "," + str(points)) # overwriting the item in the list where the old point total is with the new point total
                                        point_File = open('Points.txt', "w") # open the global points file in write mode
                                        for score in points_List: # essentially overwritting the entire file with the scores over again. Jank I know
                                            point_File.write(score + '\n')
                                        point_File.close()
                    
                                    elif len(completed) == 2: # if the file with a list of users who already completed is two...
                                        await ctx.send("You answered Third! +" + str(frame[2] + " points!"))
                                        points += int(frame[2]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        # writing the point total back in the file
                                        points_List[point_loc] = (ID + "," + str(points)) # overwriting the item in the list where the old point total is with the new point total
                                        point_File = open('Points.txt', "w") # open the global points file in write mode
                                        for score in points_List: # essentially overwritting the entire file with the scores over again. Jank I know
                                            point_File.write(score + '\n')
                                        point_File.close()
                                    else:
                                        await ctx.send("You answered! +" + str(frame[3] + " points!"))
                                        points += int(frame[3]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        # writing the point total back in the file
                                        points_List[point_loc] = (ID + "," + str(points)) # overwriting the item in the list where the old point total is with the new point total
                                        point_File = open('Points.txt', "w") # open the global points file in write mode
                                        for score in points_List: # essentially overwritting the entire file with the scores over again. Jank I know
                                            point_File.write(score + '\n')
                                        point_File.close()
                                
        
                                else:
                                    pass
                                point_loc += 1
        
                            if found == False: # if user's name is not found in the file...
                                guide = open("Challenge_" + str(num)+ "_pointBase.txt", 'r') # point framework file
                                frame = [] # list that hold the point framework for use
                                # Point file is formatted as the total number of points awarded for first, second, and third place followed by the base point total
                                for line in guide: # putting the point framework from the file into the list
                                    line = line.strip('\n') # strip off EOL character
                                    frame.append(line) # add to list
                                with open('Points.txt', "a+") as point_File: # open the global points file
                                    if len(completed) == 0: # if the file with a list of users who already completed is empty...
                                        await ctx.send("You answered first! +" + str(frame[0] + " points!")) # tell them they answer first at their first place point bonus
                                        points = int(frame[0]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        point_File.write(ID + "," + str(points)+ '\n')
                    
        
                                    elif len(completed) == 1: # if the file with a list of users who already completed is only one...
                                        await ctx.send("You answered Second! +" + str(frame[1] + " points!"))
                                        points = int(frame[1]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        point_File.write(ID + "," + str(points)+ '\n')
        
        
                                    elif len(completed) == 2: # if the file with a list of users who already completed is two...
                                        await ctx.send("You answered Third! +" + str(frame[2] + " points!"))
                                        points = int(frame[2]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        point_File.write(ID + "," + str(points)+ '\n')
                            
        
                                    else:
                                        await ctx.send("You answered! +" + str(frame[3] + " points!"))
                                        points = int(frame[3]) # add the points for completing the challenge to the current point value
                                        await ctx.send("Your current points: " + str(points)) # tell user what their current point total is
                                        
                                        point_File.write(ID + "," + str(points) + '\n')  
        
        
                    else:
                        await ctx.send("Incorrect! Try again later.")
        
                else:
                    await ctx.send("This is not in a direct message! Please submit flags via direct message.")
            except:
                await ctx.send("An error occured, were your arguments correct?")
        
        @commands.command()
        async def info(ctx, challenge): # gives info about a challenge such as point bonuses
            try:
                disp = []
                with open("Challenge_" + str(challenge)+ "_pointBase.txt") as file:
                    for line in file:
                        line = line.strip('\n')
                        disp.append(line)
                messsage = ("```Point framework for challenge " + str(challenge) + '\n' + "1st: " + disp[0] + "\n" + "2nd: " + disp[1] + "\n" + "3rd: " + disp[2] + '\n' + "Base: " + disp[3] + "```")
                await ctx.send(messsage)
            except:
                await ctx.send("An error occured, likely because the challenge does not exist.")
        
        @commands.command()
        async def leaderboard(ctx):
            try:
                channel = self.get_channel(leaderboard_channel_id) # gets the channel of wherever you want the leaderboard to be in
                base_string = '' # string that the leaderboard will get added to
                scores_dict = {} # dictionary that will hold the scores
                with open('Points.txt', "r") as points:
                    for score in points: # for each score in the file
                        # seperate the score out
                        seperate = score.find(',') 
                        username = score[0:(seperate)]
        
                        name = ctx.guild.get_member(int(username)).nick # class context.guild function get_member returns a member object which has attribute nick
                        total = score[seperate+1:] # get the raw score and strip EOL char
                        total = total.strip('\n')
        
                        scores_dict[name] = total # add the name and scores to a dictionary, with the names as keys and their score as values
                    sorted_scores = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True) # use the sorted method to sort the dictionary into a list of tuples in desceding order
                    order = 1
                    for pair in sorted_scores: # for each tuple in the list of tuples
                        name = pair[0] # grab the name
                        score = pair[1] # grab the name's corresponding score
                        base_string = base_string + str(order) + ". " + str(name) + ": " + str(score) + '\n' # add those to the base string
                        order += 1
                    await channel.send("```Score Update!" + "\n" + base_string + "```") # send the entire leaderboard as one string
            except:
                await ctx.send("An error occured while posting the leaderboard. This is most likely because the leaderboard is empty. Enter some scores!")
                
        def setup(bot):
            bot.add_cog(challenge(bot))
