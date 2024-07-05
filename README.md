# wingmanai-nomanssky
 Voice assistant for No Man's Sky powered by WingmanAI and NMS Assistant for No Man's Sky

## What Is This?
This is a repo of a config I made for No Man's Sky to use with WingmanAI by ShipBit: https://www.wingman-ai.com/.  It uses / is powered by data from the API offered by Assistant for No Man's Sky, https://nmsassistant.com/.

Basically, it allows you to speak to your "Suit" in game, give it commands in the way you normally speak, and obtain information about the No Man's Sky Universe, such as item information, crafting information, information about game updates, patches and expeditions.  The tool uses generative artificial intelligence, and, optionally, speaks back to you in a voice designed to mimic the original suit voice.

Video here: https://vimeo.com/978159719

## Quick Start

1. Download **WingmanAI**: https://www.wingman-ai.com/
2. Run the install wizard (.msi file)
3. Start the program (WingmanAI.exe) and create a free account / choose to start a free 14 day trial.
4. Close the program.
5. Navigate to **%APPDATA%/Roaming/ShipBit/WingmanAI** (your appdata is unique to your Windows user profile, so it should look something like C:\Users\{your computer user name}\AppData\Roaming\ShipBit\WingmanAI
6. Open the numbered folder, it will look something like 1_4_0 (as of this writing).  That refers to the version of Wingman.
7. Download the release files from this repo: https://github.com/teddybear082/wingmanai-nomanssky/releases/tag/wingmanai_files.
8. Unzip those release files **directly into** the numbered folder above, e.g., 1_4_0.  It will add a No Man's Sky folder to your configs folder and api_request and nms_assistant skills to your skills folder.

![image](https://github.com/teddybear082/wingmanai-nomanssky/assets/87204721/ca412c16-68a8-4f5f-b2c4-4e1d2c61d189)


![image](https://github.com/teddybear082/wingmanai-nomanssky/assets/87204721/1197d9c8-eb79-43f0-b7bc-4824351d432a)

![image](https://github.com/teddybear082/wingmanai-nomanssky/assets/87204721/96c79284-1b14-4683-9672-6eb8c85caec5)

9. To use replica "Suit Voice": download **XVAsynth from steam**: https://store.steampowered.com/app/1765720/xVASynth/ and install it.  Once installed, run it just to make sure it boots up and then close it.  Download the **Suit voice files** from this repo, here: https://github.com/teddybear082/wingmanai-nomanssky/releases/tag/xvasynth_voice_files.  Unzip those into your xVASynth install folder, where you find xVASynth.exe, for example: "C:\Program Files (x86)\Steam\steamapps\common\xVASynth".  It will add the voice to  xVASynth/resources/app/models/other.
10. Run WingmanAI (WingmanAI.exe).  Click on the **No Man's Sky folder** that you now see at the top of the interface, and click "Load".  Click on the Suit avatar picture.  Click on the **wrench** to get to settings.  Click on **"Advanced"**.  Scroll down to **Text to Speech (TTS)** as shown in the picture below. 
 Click on the **gear icon**.  Enter the **path to your xVASynth install** in the Install directory field.  **Make sure to click save** the xVASYnth TTS setting.  Then make sure to actually **click to save again to save your profile itself**.

![image](https://github.com/teddybear082/wingmanai-nomanssky/assets/87204721/56238c60-539a-46eb-bbf9-df2a00acf2d0)

![image](https://github.com/teddybear082/wingmanai-nomanssky/assets/87204721/44e81e2f-8e05-4731-a66e-9dd1f9d63b2f)

11. Try to talk to your Suit Wingman! Right now it's configured to use the "\\" key in a "Push to Talk" style, but you can click on that and set your own key in the user interface. There are also ways to have "always on" voice mode, which are covered below in Advanced Options.  Now you can start No Man's Sky and WingmanAI will be on in the background, powering your Suit!  


## What if I don't Want to Pay / Don't Want WingmanPro

The whole WingmanAI backend is open source!  You can find all the code here: https://github.com/ShipBit/wingman-ai.  You can even run it from source with python and bypass the entire .exe and UI.  Or, you can run the .exe but switch to free / local options for Speech to Text (whispercpp), LLM (choose "LocalLLM" for AI Conversation and AI Summarization Provider in the UI), and Text to Speech (xVaSynth already is local, or you can also use EdgeTTS).

What you're likely to find, though, is that there really aren't good open source AI model options that can do function calling, which powers most of the really fun things about this project, like controlling game inputs and using the NMSAssistant API.  

However, if you find a good option for local AI that can handle function calling, WingmanAI supports that!  You can change the AI provider to "LocalLLM" in the user interface and tell WingmanAI where to find it.

If, like me, you can't find a good local AI provider, you can also try Groq, which is a free LLM provider using Llama3.  The only problem is we don't know how long Groq will be free and it is rate limited. You'll need a Groq API key.

The truth is, WingmanAI can be customized extensively, and it's too detailed a subject to cover in this readme.  Hop on their discord and there are plenty of folks willing to help out!  Discord link: https://discord.gg/k8tTBar3gZ

## What if I don't want to use XVaSynth for the Suit Voice?

Sure that's fine.  In the WingmanAI UI, you can change the "Text to Speech (TTS)" setting in the settings for the Suit Wingman to another voice. If you're using Wingman Pro you can select Wingman Pro, and choose from a ton of voices.  You can also choose an Eleven Labs voice or a free EdgeTTS voice.  As stated above, the truth is, WingmanAI can be customized extensively, and it's too detailed a subject to cover in this readme.  Hop on their discord and there are plenty of folks willing to help out!  Discord link: https://discord.gg/k8tTBar3gZ

## What do you get out of this?

Nothing really, I think WingmanAI is just a super fun project and want to help people use it with their games.  Because of my early use of WingmanAI showing off a lot of custom stuff, I was invited to be a volunteer mod on their discord.  For doing that, I get a free WingmanPro sub for myself.  I don't get any sort of referral commissions or pay or anything like that.  I also contribute open-source code to the repo when I can be helpful.

## How Do I Support You If I Like This Alot?

I don't need anything! If you have a few bucks, use it to keep up a Wingman Pro sub, and toss them to the devs of the NMSAssistant API: https://buymeacoffee.com/kurt?ref=assistantNMS.  They are the real geniuses!

## I'm Having a Problem With Using This

Join the wingmanai discord and find me, I'm happy to help! https://discord.gg/k8tTBar3gZ.  You can also post issues on this github.
