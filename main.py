import discord
from discord.ext import commands 
import os
from keras.models import load_model  # TensorFlow is required for Keras to workpipenv install tensorflow==2.14.0
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

os.makedirs("./gorseller", exist_ok=True) 
intents = discord. Intents.default() 
intents.message_content = True

def get_class(model_path, labels_path, image_path):
    np.set_printoptions(suppress=True)

  
    model = load_model("keras_Model.h5", compile=False)
    with open(labels_path, "r", encoding="utf8") as file:
        class_names = file.readlines()
    
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    try:
        image = Image.open(image_path).convert("RGB")
    except IOError:
        return "Error:The image could not be opened"



    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]


    if class_name == "0 gül":
        suggestion = " daha sıcak iklimleri sever, düzenli budama, sulama ve zararlılara karşı dikkatli olmayı gerektirir. Ayrıca, daha uzun ömürlüdürler ve her yıl çiçek açarlar."
    elif class_name == "1 lale":
        suggestion = "daha soğuk havaya dayanıklı, kısa ömürlü soğanlı bitkilerdir ve genellikle daha az bakım gerektirir. Güneş ışığı, iyi drenajlı toprak ve soğuk kışlar onların sağlıklı gelişmesi için önemlidir. "
    elif class_name == "2 menekşe":
        suggestion = "Dolaylı ışık, nemli ancak su birikintisiz toprak ve ılık ortamlar menekşenin sağlıklı büyümesi için gereklidir. Dikkatli sulama ve yaprak temizliği önemlidir."
    elif class_name == "3 orkide":
        suggestion = "Dolaylı güneş ışığı, iyi hava alan toprak, nemli sıcak ortam ve düzenli ama dikkatli sulama ister. Fazla su ve doğrudan güneşten kaçının. "
    elif class_name == "4 papatya":
        suggestion = "Tam güneş ışığına bayılır, iyi drene edilmiş toprakta, serin ve nemli olmayan ortamlarda iyi büyür. Düzenli sulama ve budama yaparak daha çok çiçek açmasını sağlayabilirsiniz. "
    else:
        suggestion = f"bu bitki türü hakkında bilgim yok ({class_name})"

    return f"Prediction: {class_name}, Confidence: {confidence_score:.2f}\n{suggestion}"


bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print (f'We have logged in as {bot.user}')
@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')
####
@bot.command()
async def kaydet(ctx):
    if ctx.message.attachments:
        for attachment in ctx.message.attachments: 
            file_name = attachment.filename
            file_path = f"./gorseller/{file_name}"
            await attachment.save(file_path)
            await ctx.send(f"Görsel başarıyla kaydedildi: {file_name}")
        else:
            await ctx.send("Bir görsel yüklemelisin!")

# Görseli analiz etmek için
@bot.command()
async def check(ctx):
    files = os.listdir("./gorseller")
    if not files:
        await ctx.send("Hiçbir görsel bulunamadı, önce $kaydet ile bir görsel yükleyin!")
        return
    
    for file_name in files:
        file_path = f"./gorseller/{file_name}"

    result = get_class("keras_model.h5", "labels.txt", file_path)
    await ctx.send(f"{file_name} için sonuç:\n{result}")

bot.run("token")
