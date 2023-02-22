import { Routes, Route} from 'react-router-dom';
import AssetViewer from './components/AssetVeiwer';
import CreateAsset from './routes/assets/CreateAsset';
import Layout from './routes/Layout';
import Login from './routes/Login';
import NoMatch from './routes/NoMatch';
import User from './routes/User';
import TypeAdder from './routes/TypeAdder';
import TypeViewer from './routes/TypeViewer';
import { AuthProvider } from './hooks/useAuth';
import AssetsOverview from './routes/assets/AssetsOverview';
import SubLayout from './routes/assets/SubLayout';
import CreateProject from './routes/CreateProject';
import AdminManager from './routes/AdminManager';
import RelatedAssetViewer from './components/RelatedAssetViewer';
import Tags from './routes/Tags';
import TagViewer from './routes/TagViewer';
import ProjectViewer from './routes/ProjectViewer';
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
						<Route path="related" element={<RelatedAssetViewer canEdit={true} isNew={false}/>} />
					</Route>
					<Route path="tags/" element={<Tags />}>
						<Route path=":id" element={<TagViewer/>} />	
					</Route>
					<Route path="projects/" element={<ProjectViewer/>}>
					</Route>
					<Route path="type/" element={<SubLayout name="Types"/>}>
						<Route index element={<TypeViewer />} />
						<Route path="adder" element={<TypeAdder />} />
					</Route>
					<Route path="accounts" element={<AdminManager />} />
					<Route path="user" element={<User />} />
					<Route path="new" element={<CreateProject />} />
				</Route>
				<Route path="*" element={<NoMatch />} />
			</Routes>
		</AuthProvider>

	);
}

export default App;
