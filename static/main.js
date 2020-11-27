var app2 = new Vue({
        delimiters: ['[[', ']]'],
        el: '#tests',
        data: {
        },
        methods: {
            hi() {
                alert("Выполнилось")
            },
        }
    }
);


var app = new Vue({
        delimiters: ['[[', ']]'],
        el: '#counter',
        data: {
            answers: answers,
            cur_ans: this.answers[0]
        },
        methods: {}
    }
);

