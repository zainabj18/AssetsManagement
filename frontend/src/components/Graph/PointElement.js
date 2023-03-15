import { Component } from 'react';

class PointElement extends Component {

	constructor(props) {
		super(props);
		this.point = props.point;
		this.rotation = props.rotation;
		this.textSize = props.textSize;
		this.mouseOver = props.onMouseOver;
		this.mouseLeave = props.onMouseLeave;
		this.state = { height: 0, width: 0 };
	}

	componentDidMount() {
		this.setState({ height: this.container.clientHeight, width: this.container.clientWidth });
	}

	render() {
		return (
			<div
				ref={(e) => { this.container = e; }}
				style={{
					position: 'absolute',
					transform:
						'translate('
						+ (this.point.x - this.state.width / 2)
						+ 'px, '
						+ (this.point.y - this.state.height / 2)
						+ 'px)'
						+ this.rotation,
					fontSize: this.textSize
				}}
				onMouseOver={this.mouseOver}
				onMouseLeave={this.mouseLeave}
			>
				{this.point.name}
			</div>
		);
	};
};

export default PointElement;