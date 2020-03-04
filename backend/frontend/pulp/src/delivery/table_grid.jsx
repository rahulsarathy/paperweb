import React, { Component } from "react";
import { DeliveryRow, TableHeader, DeliveryItems } from "./components.jsx";
var Infinite = require("react-infinite");

export default class TableGrid extends Component {
	constructor(props) {
		super(props);
	}

	render() {
		return (
			<div className="table-container">
				<TableHeader />
				<DeliveryItems
					reading_list={this.props.reading_list}
					search={this.props.search}
					sort={this.props.sort}
				/>
			</div>
		);
	}
}
