import React, { Component } from 'react';

import logo from './logo.svg';
import './App.css';
import $ from 'jquery'; 


var BooksList = React.createClass({
    loadBooksFromServer: function(){
        console.log(' In ', this.props.url)
        $.ajax({
            url: this.props.url,
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
        if (this.state.data && this.state.data.results) {
            var results = this.state.data.results
            console.log('DATA!', results)
            var bookNodes = results.map(function(book, index){
                return <li key={index}> .{book.title} </li>
            })
        }
        return (
            <div>
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
            BookList
        </p>
        <BooksList url='http://sadhana-beckys57.c9users.io/api/' pollInterval={100000} />
      </div>
    );
  }
}

export default App;
