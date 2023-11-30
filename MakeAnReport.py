


def create_report(Players, NumberOfLaps, race_id):
    
    from test2 import Players as PlayersCls
    import shutil
    import os 
    import re 

    path_to_Report_dependencies = os.path.abspath("Report_dependencies") # Js and Css 
    path_to_Dependencies = os.path.abspath("Dependencies") # Avatars 
    path_to_Race_photo= os.path.abspath("RacePhoto") # Finish line photos 


    """ Create a folder for new report """
    path = os.path.abspath('Reports')
    Report_name = f'Zaznam_zavodu_{race_id}'
    Report_path = os.path.join(path, Report_name)
    try:
        os.mkdir(Report_path)
    except:
        pass

    """ Css package """
    template_path_css = os.path.join(path_to_Report_dependencies, "Styles\\style.css")
    Report_path_css = os.path.join(Report_path, "Styles")
    if os.path.exists(Report_path_css):
        pass
    else:
        os.mkdir(Report_path_css)
    shutil.copy(src=template_path_css ,dst=Report_path_css)

    """ Css package """

    """ JS package """
    template_path_js = os.path.join(path_to_Report_dependencies, "Js\\Template.js")
    Report_path_js = os.path.join(Report_path, "Js")
    if os.path.exists(Report_path_js):
        pass
    else:
        os.mkdir(Report_path_js)
    shutil.copy(src=template_path_js  ,dst=Report_path_js)

    """ Avatar package """
    Avatar_folder = os.path.join(Report_path, "avatar")
    if os.path.exists(Avatar_folder):
        pass
    else:
        os.mkdir(Avatar_folder)
    for images in os.listdir(path_to_Dependencies):
        shutil.copy(src=f'{path_to_Dependencies}\\{images}' ,dst=Avatar_folder )
    """ Avatar package """
    
    
    
    """Race photos """
    race_photos_path = os.path.join(Report_path, "Race_photos")
    os.mkdir(race_photos_path)
   
    for player in Players:
        tag = player.tag
        for folder in os.listdir(path_to_Race_photo):
            if folder == tag: 
                tag_path = os.path.join(path_to_Race_photo, tag)
                for img in os.listdir(tag_path):
                    match = re.search(r'\d+', img)
                    if int(match.group()) == race_id and img[-7:] != "raw.jpg":
                            shutil.copy(src=os.path.join(tag_path,img), dst=os.path.join(race_photos_path, img))

    """Race photos """

    """ Load Data to generate report """

    

    winner_list = []
    temp_list = [] 
    for obj in Players: 
        score = round((obj.Score[-1])[1] - (obj.Score[0])[1],3)
        temp_list.append([obj._nick, score])
    for i in range(len(temp_list)):
        if i == 0:
            winner_list.append(temp_list[i])
        else:
            for j in range(len(winner_list)):
                if temp_list[i][1] < winner_list[j][1]:
                    winner_list.insert(j, temp_list[i] )
                    break 
            else:
                winner_list.append(temp_list[i])

# Winner list _ serazeni hraci od nejlepsiho po nejhorsi dle celkovych casu, [ jmeno, celkovy cas]
#  obj in Players.relativeScore == score do html tabulky 

    pass

    """CREATE TABLE """ 
    
    table_html = "<table>\n<tr>\n" 
    
    
    for idx, obj in enumerate(winner_list):
        tag = PlayersCls.GetPlayerTagByNick(obj[0])
        if idx == len(winner_list)-1:
            table_html += f"<th><img src=avatar/{tag}.jpg width=125 height=100></th>\n</tr>\n"
        else:
            table_html += f"<th><img src=avatar/{tag}.jpg width=125 height=100></th>\n"
    table_html += "</tr>\n"
  
    
    for idx, player in enumerate(winner_list):

        if idx == 0:
            table_html += f"<th id=first>{idx+1}.  {player[0]}</th>\n"
        elif idx == 1:
            table_html += f"<th id=second>{idx+1}.  {player[0]}</th>\n"
        elif idx == 2:
            table_html += f"<th id=third>{idx+1}.  {player[0]}</th>\n"
        elif idx == len(Players)-1:
            table_html += f"<th>{idx+1}.  {player[0]}</th>\n</tr>\n"
        else:
            table_html += f"<th>{idx+1}.  {player[0]}</th>\n"
            
    table_html += "</tr>\n<tr>\n"
    
    
    for i, player in enumerate(winner_list):
        name = player[0]
        color = PlayersCls.GetPlayerTagByNick(desired_nick= name)
        score = PlayersCls.GetPlayerObjByNick(desired_nick=name).relativeScore
        
    
        
        for j, item in enumerate( score ):
            if j == 0:
                table_html += "<td>\n"
                table_html += f"<div id=score{i+1}>\n"
                table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
            elif j == len( score )-1:
                table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
                table_html += "</div>\n"
                table_html += "</td>"
            else:
                table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
        
        
    # for i, pack in enumerate(zip(nick,color_list_html,records)):
    #     name = pack[0]
    #     color = pack[1]
    #     record = pack[2:]
    #     for j, item in enumerate(record[0]):
    #         if j == 0:
    #             table_html += "<td>\n"
    #             table_html += f"<div id=score{i+1}>\n"
    #             table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
    #         elif j == len(record[0])-1:
    #             table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
    #             table_html += "</div>\n"
    #             table_html += "</td>"
    #         else:
    #             table_html += f"<div id=col{i+1}row{j+1} data-info={name},{color},{item[0]} >Kolo: {item[0]}...Cas: {item[1]} s </div>\n"
                
        
    table_html += "</tr>\n</table>\n"

    

    import datetime
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    """CREATE TABLE """ 



    # Create the HTML content using string concatenation
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Zaznam zavodu</title>
        <link rel="stylesheet" type="text/css" href="Styles/style.css">
        <script src="Js/Template.js"></script>
        <div id="raceID" data-info={race_id}></div>
        <div id="numOfPlayers" data-info={len(winner_list)}></div>
    </head>

    <body>

        <h1 id="title">Vysledky zavodu</h1>
    
        <br><br>
        <ul id="list">
            <li>Cas vytvoreni: {formatted_datetime}</li>
            <li>Pocet zavodniku: {len(Players)}</li>
            <li>Pocet kol: {NumberOfLaps}</li>
        </ul>
        <hr>
        <br>
        <h2 id="title2">Celkovy Zaznam Zavodu </h2>
        <br><br><br>
        {table_html}
        <div id="modal" class="modal">
            <div class="modal-content">
            <img id="modal-image" src="" alt="Your Image">
        </div>

    </body>
    </html>
    """
    html_report_path = os.path.join(Report_path,f'Zaznam_zavodu_{race_id}.html')
    with open(html_report_path , 'w') as file:
        file.write(html_content)

    print("Static HTML report generated successfully.")