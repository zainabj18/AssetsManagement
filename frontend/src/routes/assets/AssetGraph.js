import { Box } from '@chakra-ui/react';

// install (please make sure versions match peerDependencies)
// yarn add @nivo/core @nivo/network
import { ResponsiveNetwork } from '@nivo/network';
import data from './mock_tags.json';
const MyResponsiveNetwork = ({ data /* see data tab */ }) => (
	<ResponsiveNetwork
		data={data}
		margin={{ top: 0, right: 0, bottom: 0, left: 0 }}
		linkDistance={function(e){return e.distance;}}
		centeringStrength={1.2}
		repulsivity={19}
		iterations={260}
		nodeSize={function(n){return n.size;}}
		activeNodeSize={function(n){return 1.5*n.size;}}
		nodeColor={function(e){return e.color;}}
		nodeBorderWidth={4}
		nodeBorderColor={{
			from: 'color',
			modifiers: [
				[
					'darker',
					0.8
				]
			]
		}}
		linkThickness={function(n){return 2+2*n.target.data.height;}}
		linkBlendMode="multiply"
		motionConfig="wobbly"
	/>
);
const AsssetGraph = () => {
	return (<div style={{height: '100vh',width: '100vw'}}>
		<MyResponsiveNetwork data={data}/>
	</div> );
};
 
export default AsssetGraph;