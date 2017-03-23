
import React from 'react';
import 'whatwg-fetch'
// import {
//   AppRegistry,
//   StyleSheet,
//   Text,
//   View,ScrollView,
// } from 'react-native';


class Formy extends React.Component {
  
  constructor(props) {
    super(props);
    
    this.state = {
      'gps_n': '100',
      gps_e: '200',
      water_seasonality: true,
      id: this.props.id,
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  
  loadState() {
    this.setState({
      gps_n: '100',
      gps_e: '200',
    })
  }
  
  handleChange(event) {
    // If all necessary fields are filled then call handleSubmit
    const target = event.target;
    const value = target.type === 'checkbox' ? target.checked : target.value;
    const name = target.name;

    this.setState({
      [name]: value
    });
  }

  handleSubmit(event) {
    alert('Your favorite flavor is: ' + this.state.value);
    event.preventDefault();
    
    var c =fetch('https://sadhana-beckys57.c9users.io/api/d1/save/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: 'Hubot',
        login: 'hubot',
      })
    }).then(response => console.log(response))
  }
  
  
  render() {
	  return (
		  <form onSubmit={this.handleSubmit}>
		  	Tree number: <br/>
		  	
		  	<label htmlFor="person">Person:</label>
		  	<select value="1" onChange={this.handleChange} id="person" name="person">
		  		<option value="">---------</option>
		  		<option value="1">Beatrice Chepngetish</option>

		  	</select><br/>
		  	<label htmlFor="species">Species:</label>
		  	<select value="0" onChange={this.handleChange} id="species" name="species">
		  		<option value="0">Syzygium guineense</option>
		  		<option value="1">Juniperus procera</option>

		  	</select><br/>
		  	<label htmlFor="gps_n">Gps n:</label><input onChange={this.handleChange} id="gps_n" defaultValue={this.props.id} maxLength="15" name="gps_n" type="text" /><br/>
		  	<label htmlFor="gps_e">Gps e:</label><input onChange={this.handleChange} id="gps_e" defaultValue={this.props.id} maxLength="15" name="gps_e" type="text" /><br/> 
		  	
		  	<label htmlFor="water_seasonality">Water seasonality:</label><input onChange={this.handleChange} id="water_seasonality" name="water_seasonality" type="checkbox" /><br/>
		  	
		  	<label htmlFor="water_distance">Water distance:</label><input onChange={this.handleChange} id="water_distance" maxLength="50" name="water_distance" type="text" /><br/>
		  	<label htmlFor="notes">Notes:</label><textarea cols="40" id="notes" name="notes" rows="10"></textarea><br/>
		  	<input id="id" name="id" type="hidden" defaultValue="" /><br/>
		  	
		  	<input type="submit" />
		  </form>
		  
	  );
	}
}


export default Formy;