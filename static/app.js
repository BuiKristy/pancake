/*Vue.directive('sortable', {
    inserted: function(el, binding) {
        $(el).sortable({
            axis: "y", 
            containment: "parent", 
            tolerance: "pointer",
            stop: function(event, ui) {
                console.log($(el).children().toArray().map(function(value) {
                    return value.innerText;
                }));
            }
        });
        $(el).disableSelection();
    },

    bind: function() {
        console.log(this);
    },

    componentUpdated: function(el) {
        $(el).sortable("refresh");
        console.log(el);
    }
})*/

var app = new Vue ({
    el: "#app",
    data: {
        model: {"playlists": []}
    },
    methods: {
        refreshModel: function() {
            app_ref = this;
            var get_model = $.getJSON("/model").done(function(data) {
                app_ref.model = data;
            });
        },

        localChangeSong: function(index, arr, start_index, end_index) {
            this.model.playlists[index].songs = arr;
            console.log(this)

            $.ajax({
                method: 'PATCH',
                url: '/playlists/' + this.model.playlists[index].id + '/' + start_index,
                data: {new_index: end_index}
            }).done(function() {
                console.log("hi there");
            })
        }
    }
})

Vue.component('playlist-item', {
    props: ['playlistInfo', 'index'],
    computed: {
        ul_id : function() {
            return 'playlist' + this.playlistInfo.id
        }
    },
    template: '<div><h3>{{ playlistInfo.name }}</h3> <sortable v-on:sortable-change="echo" v-bind:song-list="playlistInfo.songs"' +
        'v-bind:index="index"></sortable></div>',
    methods:  {
        echo: function(index, arr, start_index, end_index) {
            this.$emit('sortable-change', index, arr, start_index, end_index);
        }
    }
})

Vue.component('sortable', {
    props: ['songList', 'index'],
    template: '<ul><li v-for="song in songList">{{ song }}</li></ul>',
    mounted: function() {
        var vm = this;
        console.log(this.index);
        $(this.$el)
            .sortable({
                axis: "y", 
                containment: "parent", 
                tolerance: "pointer",
                stop: function(event, ui) {
                    console.log($(vm.$el).children().toArray().map(function(value) {
                        return value.innerText;
                    }));
                    x = $(vm.$el).children().toArray().map(function(value) {
                        return value.innerText;
                    });
                    end_index = ui.item.index();
                    $(vm.$el).sortable("cancel");
                    start_index = ui.item.index();
                    vm.$emit('sortable-change', vm.index, x, start_index, end_index)
                }
            })
            .disableSelection();
    }
})

$(function() {

});