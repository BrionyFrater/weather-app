import datetime
import requests
from tkinter import *


def getWeather(event):

    global weatherIcon
    
    #knowingly exposed, free subscription only for this project 
    apiKey = "a488b4cf3ec42e1e0ea576120413ea4f"
    place = placeEntry.get()

    url = f"https://api.openweathermap.org/data/2.5/weather?q={place}&appid={apiKey}&units=metric"
    
    data = requests.get(url)
    weatherData = data.json()

    
    if(weatherData["cod"]=="404"):
        placeEntry.delete(0, END)
        placeEntry.insert(0, weatherData["message"])
    else:
        name = weatherData["name"] +","+ weatherData["sys"]["country"]

        tinfo = weatherData["timezone"]

        timezone = datetime.timezone(datetime.timedelta(seconds=tinfo))
        time = datetime.datetime.now(timezone).strftime("%B %d, %Y %I:%M %p")
        
        weather = weatherData["weather"][0]["main"]
        des = weatherData["weather"][0]["description"]
        temp = round(weatherData["main"]["temp"])
        icon = weatherData["weather"][0]["icon"]

        wind = weatherData["wind"]["speed"]
        humid = weatherData["main"]["humidity"]
        pres = weatherData["main"]["pressure"]
        cloud = weatherData["clouds"]["all"]


        weatherIcon = PhotoImage(file="icons/"+str(icon)+"@2x.png")
        canvas.itemconfig(weaIcon, image=weatherIcon)
        
        
        #change background according to weather
        match(weather):
            case "Clear":
                canvas.itemconfig(bgWindow, image=clear)
            case "Clouds":
                canvas.itemconfig(bgWindow, image=clouds)
            case "Drizzle" | "Rain":
                canvas.itemconfig(bgWindow, image=rain)
            case "Snow":
                canvas.itemconfig(bgWindow, image=snow)
            case "Thunderstorm":
                canvas.itemconfig(bgWindow, image=thunder)
            case _:
                canvas.itemconfig(bgWindow, image=athmos)
                
        
        #change canvas text
        canvas.itemconfig(wLoc, text=name)
        canvas.itemconfig(tem, text=str(temp)+"°C")
        canvas.itemconfig(wCon, text=str(des))

        canvas.itemconfig(wWin, text="Wind Speed: "+str(wind)+ "m/s")
        canvas.itemconfig(wHum, text="Humidity: "+str(humid)+ "%")
        canvas.itemconfig(wPres, text="Pressure: "+str(pres)+ "hPa")
        canvas.itemconfig(wClouds, text="Cloudiness: "+str(cloud)+ "%")

        canvas.itemconfig(tim, text=time)
        
        
        canvas.itemconfig(menu, image=menuImg)
        


window = Tk()
window.geometry("350x550+1400+100")
window.resizable(False, False)
window.title("Weather")
windowIcon = PhotoImage(file="icons/02d@2x.png")
window.iconphoto(True, windowIcon)

#backgrounds
clear = PhotoImage(file="backgrounds/clear.png")
clouds = PhotoImage(file="backgrounds/clouds.png")
rain = PhotoImage(file="backgrounds/rain.png")
thunder = PhotoImage(file="backgrounds/thunder.png")
athmos = PhotoImage(file="backgrounds/athmosphere.png")
snow = PhotoImage(file="backgrounds/snow.png")

canvas = Canvas(window, height=500, width=300, highlightthickness=0)
bgWindow = canvas.create_image(0,0, image=clear, anchor="nw")
canvas.pack(fill="both", expand=True, pady=0)

#info text labels
wLoc = canvas.create_text(175,100, font=("Arial", 10), fill="#FFFFFF")
tem = canvas.create_text(175,150, font=("Arial", 50), fill="#FFFFFF")
wCon = canvas.create_text(175,210, font=("Arial", 12), fill="#FFFFFF")

wWin = canvas.create_text(175,360, font=("Arial", 10), fill="#FFFFFF")
wHum = canvas.create_text(175,380, font=("Arial", 10), fill="#FFFFFF")
wPres = canvas.create_text(175,400, font=("Arial", 10), fill="#FFFFFF")
wClouds = canvas.create_text(175,420, font=("Arial", 10), fill="#FFFFFF")

tim = canvas.create_text(138,515, font=("Arial", 9), fill="#FFFFFF")

weaIcon = canvas.create_image(175, 300)
canvas.pack()

#menubar
menuImg = PhotoImage(file="icons/menubar.png")
menu = canvas.create_image(175, 350)


#lines
lineImg = PhotoImage(file="icons/line.png")
canvas.create_image(175, 370, image=lineImg)
canvas.create_image(175, 390, image=lineImg)
canvas.create_image(175, 410, image=lineImg)
canvas.create_image(175, 430, image=lineImg)

canvas.create_image(175, 500, image=lineImg)
canvas.pack()


#searchbar
searchImg = PhotoImage(file="icons/searchbar.png")
canvas.create_image(175, 55, image=searchImg)
canvas.pack()

placeEntry = Entry(window, font=("Arial, 10"), bd=0)
placeEntry.insert(0,"bridgetown, bb")
placeEntry.focus()

entryWindow = canvas.create_window(175, 55, window=placeEntry)

#bind get weather to enter key
window.bind("<Return>",getWeather)
window.mainloop()
