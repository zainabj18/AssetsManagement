import { Component } from 'react';

class PointElement extends Component {

	constructor(props) {
		super(props);
		this.point = props.point;
		this.rotation = props.rotation;
		this.textSize = props.textSize;
		this.mouseOver = props.onMouseOver;
		this.mouseLeave = props.onMouseLeave;
		this.spacing = props.spacing;
		this.state = { height: 0, width: 0 };
	}

	getOffSetX() {
		let translation = (this.state.width + this.spacing) / 2 * Math.cos(this.rotation.angle);
		return ((this.rotation.flipped) ? -translation : translation);
	}

	getOffSetY() {
		let translation = (this.state.width + this.spacing) / 2 * Math.sin(this.rotation.angle);
		return ((this.rotation.flipped) ? -translation : translation);
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
						+ (this.point.x - this.state.width / 2 + this.getOffSetX())
						+ 'px, '
						+ (this.point.y - this.state.height / 2 + this.getOffSetY())
						+ 'px)'
						+ 'rotate(' + this.rotation.angle + 'rad)',
					fontSize: this.textSize,
					color: this.point.fontColour
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