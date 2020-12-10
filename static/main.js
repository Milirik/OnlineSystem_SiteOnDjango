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
        filters:{
            cut: function (value){
                if(!value) return ''
                value = value.toString()
                return value.split('/').pop()
            }
        }

    }
);

