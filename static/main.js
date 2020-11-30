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
            status_colors: {
                "All tests passed": "green",
                "Error": "red"
            }
        },
        methods: {
        },

    }
);

