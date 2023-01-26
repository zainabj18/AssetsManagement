import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/CreateAsset';
import Layout from './routes/Layout';
import NoMatch from './routes/NoMatch';

function App() {
	return (
		<Routes>
			<Route path="/" element={<Layout />}>
				<Route path="newasset" element={<CreateAsset />} />
				<Route path="asset/:id" element={<AssetViewer canEdit={true} isNew={false}/>} />
				<Route path="*" element={<NoMatch />} />
			</Route>
		</Routes>
	);
}

export default App;
