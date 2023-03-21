import gradio as gr
import pandas

table = None
rows = None
result = None
message = None

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(
        placeholder='Enter command'
    )


    def user_input(user_message, history):
        global table
        global rows
        global result
        global message

        result = user_message.split()
        message = user_message

        if len(result) == 2 and user_message not in (
                'decision classes',
                'classes size'
        ):
            user_message = result
            table = pandas.read_csv(user_message[0])
            rows = user_message[1]
            user_message \
                = f'Show {user_message[1]} ' \
                  f'rows of this table:<br><br>' \
                  f'{table.to_csv(index=False)}' \
                .replace('\r\n', '<br>')

        return '', history + [[user_message, None]]


    def bot_respond(history):
        bot_message = ''

        if len(result) == 2 and message not in (
                'decision classes',
                'classes size'
        ):
            if rows.isdigit() and int(rows) > 0:
                if int(rows) > table.shape[0]:
                    bot_message = f'Given table doesn\'t ' \
                                  f'have so many rows ' \
                                  f'({rows}).<br>' \
                                  f'Displaying whole ' \
                                  f'table:<br><br>'

                bot_message += table.iloc[:int(rows), :] \
                    .to_csv(index=False)
                bot_message += \
                    f'<br>Moreover, this table ' \
                    f'has {table.shape[0]} ' \
                    f'objects and ' \
                    f'{table.shape[1] - 1} ' \
                    f'attributes'

            else:
                bot_message = f'Wrong rows number ({rows})'

        elif message == 'decision classes':
            classes = pandas.unique(table.iloc[:, -1])
            bot_message = \
                f'Given table contains {len(classes)} ' \
                f'decision classes'

        elif message == 'classes size':
            column = table.iloc[:, -1]
            counter = 0
            classes = pandas.unique(column)
            bot_message = \
                f'Here are sizes of following classes:' \
                f'<br>'

            for given in classes:
                for which, item in column.items():
                    if item == given:
                        counter += 1

                bot_message += f'{given}-{counter}<br>'
                counter = 0

        history[-1][1] = bot_message

        return history


    msg.submit(
        user_input,
        [msg, chatbot],
        [msg, chatbot],
        queue=False
    ) \
        .then(
        bot_respond,
        chatbot,
        chatbot
    )

demo.launch()
