import requests
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

API_KEY = ""


def clear_entry(event):
    entry.delete(0, END)


def display_weather(city):
    try:
        url = f"https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)
        data = response.json()

        if "error" in data:
            label.config(text=data["error"]["message"], font=("Helvetica", 12))  # Adjust font size
        else:
            temp = data["current"]["temp_c"]
            wind = data["current"]["wind_kph"]
            prep = data["current"]["precip_mm"]
            vis = data["current"]["vis_km"]
            condition = data["current"]["condition"]["text"]
            icon_url = data["current"]["condition"]["icon"]

            label.config(text=f"Currently, it is {temp} degrees Celsius in {city}.\n"
                              f"\nWind is blowing at {wind} Km/h.\n"
                              f"\nPrecipitation: {prep} mm.\n"
                              f"\nVisibility is {vis} Km.\n"
                              f"\nCondition is {condition}.", font=("Helvetica", 16))  # Adjust font size

            fetch_and_display_icon(icon_url)
    except requests.exceptions.RequestException as e:
        label.config(text=f"An error occurred: {str(e)}", font=("Helvetica", 14))  # Adjust font size


def fetch_and_display_icon(icon_url):
    try:
        icon_url = icon_url.replace("//", "https://")
        response = requests.get(icon_url)

        if response.status_code == 200:
            img_data = Image.open(BytesIO(response.content))
            img = ImageTk.PhotoImage(img_data)
            image_label.config(image=img)
            image_label.image = img  # Keep a reference to prevent image garbage collection
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the weather icon: {str(e)}")


def main():
    root = Tk()
    root.title("Weather Forecast")

    global entry, label, image_label
    label = Label(root, text="", wraplength=300, font=("Helvetica", 12))  # Adjust font size
    label.pack(padx=10, pady=10)

    image_label = Label(root)
    image_label.pack(padx=10, pady=10)

    entry = Entry(root, width=30, font=("Helvetica", 12))  # Adjust font size
    entry.pack(padx=50, pady=50)
    entry.insert(0, "Enter city name")
    entry.bind("<FocusIn>", clear_entry)

    button = Button(root, text="Get Weather", command=lambda: display_weather(entry.get()))
    button.pack(padx=30, pady=30)

    # Bind the Enter key to trigger the Get Weather button
    entry.bind("<Return>", lambda event=None: button.invoke())

    root.mainloop()


if __name__ == "__main__":
    main()
