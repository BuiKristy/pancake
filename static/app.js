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

var store = {

}

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

            $.ajax({
                method: 'PATCH',
                url: '/playlists/' + this.model.playlists[index].id + '/' + start_index,
                data: {new_index: end_index}
            }).done(this.refreshModel)
        },

        localChangeName: function(index, new_name) {
            this.model.playlists[index].name = new_name;

            $.ajax({
                method: 'PATCH',
                url: '/playlists/' + this.model.playlists[index].id,
                data: {playlist_name: new_name}
            }).done(function() {
                console.log("renamed playlist");
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
    template: '<div><h3 v-if="!editing">{{ playlistInfo.name }}</h3> <input v-else v-bind:value="playlistInfo.name" v-on:input="namePlaylist"> <button v-on:click="editPlaylistName"></button> <sortable v-on:sortable-change="echo"' +
        'v-bind:song-list="playlistInfo.songs"></sortable></div>',
    methods:  {
        echo: function(arr, start_index, end_index) {
            this.$emit('sortable-change', this.index, arr, start_index, end_index);
        },

        editPlaylistName: function() {
            this.editing = !this.editing;
        },

        namePlaylist: function(new_name) {
            this.$emit('edit-playlist', this.index, new_name.target.value)
        }
    },
    data: function() {
        return {
            editing: false
        }
    }
})

Vue.component('sortable', {
    props: ['songList'],
    template: '<ul><li v-for="song in songList">{{ song }}</li></ul>',
    mounted: function() {
        var vm = this;
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
                    vm.$emit('sortable-change', x, start_index, end_index)
                }
            })
            .disableSelection();
    }
})

$(function() {

});