/** @jsx React.DOM */

var SearchCountingWords = React.createClass({
    getInitialState: function () {
        return {value: ''};
    },
    handleChange: function (e) {
        this.setState({value: e.target.value});
    },
    render: function () {
        var textString = this.state.value.trim().toLowerCase(),
            w = [];

        if (textString.length > 0) {
            var arrText = textString.match(/([а-яА-ЯёЁA-Za-z0-9-])+/g),
                words = {};

            for (var word in arrText) {
                var count = arrText.filter(function (a) {
                    return [arrText[word]].indexOf(a) > -1;
                }).length;
                words[arrText[word]] = count;

            }
            for(var word in words){
                w.push({'name': word, 'count': words[word]});
            }
        }
        return (
            <div className="SearchCountingWords">
                <textarea
                    onChange={this.handleChange}
                    ref="textarea"
                    defaultValue={this.state.value}
                    placeholder="Type your text."
                />
                <h3>Contained in the text of words and their frequency of repetition.</h3>
                <ul
                    className="content">
                    { w.map(function(l){
                            return <li>{l.name} <span>{l.count}</span></li>
                        }) }
                </ul>
            </div>
        );
    }
});

React.render(<SearchCountingWords />, document.getElementById('form'));