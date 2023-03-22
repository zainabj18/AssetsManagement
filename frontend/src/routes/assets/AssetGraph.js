// install (please make sure versions match peerDependencies)
// yarn add @nivo/core @nivo/network
import { ResponsiveNetwork } from '@nivo/network';
import { BasicTooltip } from '@nivo/tooltip';
import { useEffect, useState } from 'react';
import { getAssetsGraphData } from '../../api';
const ToolTip = (props) => {
	return (
		<BasicTooltip
			id={props.node.id}
			value={props.node.data.degree}
		/>
	);
};
const MyResponsiveNetwork = ({ data /* see data tab */ }) => (
	<ResponsiveNetwork
		data={data}
		margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
		linkDistance={100}
		linkColor={function (e) { return ((e.target.size < 5) ? 'orange' : 'blue'); }}
		nodeSize={function (n) {
			let size = 25 * n.size;
			if (size > 50) {
				return 50;
			}
			return size;
		}}
		nodeColor={function (e) { return e.color; }}
		linkThickness={function (e) { return ((e.source.size < 5 && e.target.size < 5) ? 0 : 1); }}
		nodeTooltip={ToolTip}
		onClick={(e) => console.log(e)}
		centeringStrength={0.1}
		repulsivity={500}
		inactiveNodeSize={4}
		activeNodeSize={50}
		linkBlendMode={'luminosity'}
		motionConfig={'slow'}
	/>
);

const AsssetGraph = () => {

	const [data, set_data] = useState();

	useEffect(() => {
		getAssetsGraphData().then(data => {
			console.log(data);
			set_data(data);
		});
	}, []);

	return (data && <div style={{ height: '1000px', width: '100vw'}}>
		<MyResponsiveNetwork data={data} />
	</div>);
};

export default AsssetGraph;