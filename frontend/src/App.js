import { Routes, Route, NavLink } from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/assets/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import AssetSearcher from './routes/AssetSearcher';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import TypeViewer from './routes/TypeViewer';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import SubLayout from './routes/assets/SubLayout';
import AssetList from './components/AssetList';
import CreateProject from './routes/CreateProject';
import { Button } from '@chakra-ui/react';
//TODO:Wrap in error boundary
function App() {

	return (
		<AuthProvider>
			<Routes>
				<Route path="/login" element={<Login />} />
				<Route path="/" element={<Layout />}>
					<Route path="assets/" element={<SubLayout name="Assets"/>}>
						<Route index element={<AssetsOverview />} />
						<Route path="new" element={<CreateAsset />} />
						<Route path="view/:id" element={<AssetViewer canEdit={true} isNew={false}/>} />
					</Route>
					<Route path="projects/" element={<SubLayout name="Proejcts"/>}>
						<Route index element={<NavLink to="./new">Create New Project</NavLink>} />
						<Route path="new" element={<CreateProject />} />
					</Route>
					<Route path="type/" element={<SubLayout name="Types"/>}>
						<Route index element={<TypeViewer />} />
						<Route path="adder" element={<TypeAdder />} />
					</Route>
					<Route path="user" element={<User />} />
				</Route>
				<Route path="*" element={<NoMatch />} />
			</Routes>
		</AuthProvider>

	);
}

export default App;
