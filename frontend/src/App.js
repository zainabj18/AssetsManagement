import { Routes, Route } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/assets/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import FilterBasedSearch from './routes/FilterBasedSearch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import AssetsLayout from './routes/assets/AssetsLayout';
import RelatedAssetViewer from './components/RelatedAssetViewer';



function App() {
	
	return (

		<Routes>
			<Route path="/login" element={<Login />} />
			<Route path="/" element={<Layout />}>
				<Route path="assets/" element={<AssetsLayout />}>
					<Route index element={<AssetsOverview />} />
					<Route path="new" element={<CreateAsset />} />
					<Route path="view/related/:id" element={<RelatedAssetViewer canEdit={true} isNew={false}/>} />
				</Route>
				<Route path="filter" element={<FilterBasedSearch />} />
				<Route path="user" element={<User />} />
				<Route path="type/adder" element={<TypeAdder />} />
			</Route>
			<Route path="*" element={<NoMatch />} />
		</Routes>

	);
}

export default App;
