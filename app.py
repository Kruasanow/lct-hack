from flask import Flask, render_template, request
import json

app = Flask(__name__)

def transform_str(resArr):
    if '| )' in resArr:
        resArr = resArr.replace(' | )', ') | ')
    if '& )' in resArr:
        resArr = resArr.replace(' & )', ') & ')
    return resArr

def res_arr_form_maker(resArr):
    # print(resArr)
    res_string = ''
    try:
        for i in resArr:
            if '|' in i:
                i = i.replace(' |','')
                res_string += f"({i}) | "
            elif '&' in i:
                i = i.replace(' &','')
                res_string += f"({i}) & "
            elif '(' in i:
                res_string+='('
            elif ')' in i:
                res_string+=')'
            else:
                print('ne I ne & ne srabotalo')
        # print(res_string[:-2])
    except Exception:
        pass
    return transform_str(res_string[:-2])

@app.route('/', methods=['GET', 'POST'])
def index():
    entered_values = []

    if request.method == 'POST':
        priority = request.form.get('prioritySelect')
        task_name = request.form.get('taskname')
        # lvl_select = request.form.get('LvlSelect')
        resArr = request.form.get('resArr')
        selected_levels = request.form.getlist('levels')
        
        if resArr:
            resArr = json.loads(resArr)
        else:
            resArr = []
        entered_values.extend([task_name, priority, res_arr_form_maker(resArr),  selected_levels])
        print(entered_values)
    return render_template('index.html', entered_values=entered_values)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
