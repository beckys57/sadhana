import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import $ from 'jquery'; 


var BooksList = React.createClass({
    loadBooksFromServer: function(){
        console.log(' In ', this.props.url)
        $.ajax({
            url: 'http://sadhana-forest-beckys57.c9users.io/api/',// this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                console.log('Got ')
                this.setState({data: data});
            }.bind(this)
        })
    },

    getInitialState: function() {
        return {data: []};
    },

    componentDidMount: function() {
        this.loadBooksFromServer();
        setInterval(this.loadBooksFromServer, 
                    this.props.pollInterval)
    }, 
    render: function() {
        if (this.state.data) {
            console.log('DATA!', this.state)
            var bookNodes = this.state.data.map(function(book, index){
                return <li key={index}> .{book.title} </li>
            })
        }
        return (
            <div>
                <h1>Hello React!</h1>
                <ul>
                    {bookNodes}
                </ul>
            </div>
        )
    }
})

class App extends Component {
  render() {
    return (
      <div className="App">
        <div className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h2>Welcome to React</h2>
        </div>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <BooksList url='/api/' pollInterval={100000} />
      </div>
    );
  }
}

export default App;
