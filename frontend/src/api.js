import axios from 'axios';
axios.defaults.baseURL = '/api/v1';

export const loginUser = async ({ username, password }) => {
	return await axios.post('/auth/login', { username, password }).then(res => res.data);
};

export const indentifyUser = async () => {
	return await axios.get('/auth/identify').then(res => res.data);
};
export const logoutUser = async () => {
	return await axios.delete('/auth/logout').then(res => res.data);
};
export const fetchAsset = async (id) => {
	return await axios.get(`/asset/${id}`).then(res => res.data);
};
export const fetchAssetClassifications = async () => {
	return await axios.get('/asset/classifications').then(res => res.data);
};

export const fetchTags = async () => {
	return await axios.get('/tag/').then(res => res.data);
};
export const createTag = async (tag) => {
	return await axios.post('/tag/', { 'name': tag }).then(res => res.data);
};
export const removeFromTag = async (id, assets) => {
	console.log(assets, 'hello');
	return await axios.post('/tag/remove', { 'toTagID': id, 'assetIDs': assets }).then(res => res.data);
};
export const copyToTag = async (id, assets) => {
	return await axios.post('/tag/copy', { 'toTagID': id, 'assetIDs': assets }).then(res => res.data);
};
export const deleteTag = async (id) => {
	return await axios.delete(`/tag/${id}`).then(res => res.data);
};
export const fetchProjects = async () => {
	return await axios.get('/project/').then(res => res.data);
};

export const fetchAllProjects = async () => {
	return await axios.get('/project/allProjects').then(res => res.data);
};

export const fetchAllTypes = async () => {
	return await axios.get('/type/allTypes').then(res => res.data);
};

export const fetchAllAttributes = async () => {
	return await axios.get('/type/allAttributes').then(res => res.data);
};

export const createAttribute = async (newAttribute) => {
	return await axios.post('/type/adder/new', newAttribute).then(res => res.data);
};

export const createType = async (newType) => {
	return await axios.post('/type/new', newType).then(res => res.data);
};

export const fetchTypesList = async () => {
	return await axios.get('/type/names').then(res => res.data);
};
export const fetchTypesNamesVersionList = async () => {
	return await axios.get('/type/version/names').then(res => res.data);
};


export const fetchType = async (id) => {
	return await axios.get(`/type/${id}`).then(res => res.data);
};

export const createAsset = async (asset) => {
	return await axios.post('/asset/', asset).then(res => res.data);
};

export const fetchAssetProjects = async (id) => {
	return await axios.get(`/asset/projects/${id}`).then(res => res.data);
};
export const fetchAssetLinks= async (id)=> {
	return await axios.get(`/asset/links/${id}`).then(res=>res.data);
};

export const fetchRelatedTags= async (id)=> {
	return await axios.get(`/asset/related/tags/${id}`).then(res=>res.data);
};
export const fetchRelatedProjects= async (id)=> {
	return await axios.get(`/asset/related/projects/${id}`).then(res=>res.data);
};
export const fetchRelatedClassification= async (id)=> {
	return await axios.get(`/asset/related/classification/${id}`).then(res=>res.data);
};

export const fetchRelatedType= async (id)=> {
	return await axios.get(`/asset/related/type/${id}`).then(res=>res.data);
};
export const fetchRelatedFrom= async (id)=> {
	return await axios.get(`/asset/related/from/${id}`).then(res=>res.data);
};
export const fetchRelatedTo=async (id)=> {
	return await axios.get(`/asset/related/to/${id}`).then(res=>res.data);
};
export const deleteAsset = async (id) => {
	return await axios.delete(`/asset/${id}`).then(res => res.data);
};

export const deleteProject = async (id) => {

	console.log(id);
	return await axios.post(`/project/delete/${id}`).then(res => res.data);
};

export const fetchAssetSummary = async () => {
	return await axios.get('/asset/summary').then(res => res.data);
};

export const updateAsset = async (id, asset) => {
	return await axios.patch(`/asset/${id}`, asset).then(res => res.data);
};
export const createProject = async (project) => {
	console.log(project);
	return await axios.post('/project/new', project).then(res => res.data);
};

export const updateTag = async (id, tag) => {
	return await axios.patch(`/tag/${id}`, tag).then(res => res.data);
};
export const fetchAssetsinTag = async (id) => {
	return await axios.get(`/asset/tags/summary/${id}`).then(res => res.data);
};

export const fetchAssetsLogs= async (id) => {
	return await axios.get(`/asset/logs/${id}`).then(res => res.data);
};
export const deleteType = async (id) => {
	return await axios.post(`/type/delete/${id}`).then(res => res.data);
};
export const deleteAttribute = async (id) => {
	return await axios.post(`/type/attribute/delete/${id}`).then(res => res.data);
};
export const isAttributeNameIn = async (name) => {
	return await axios.post('/type/adder/isAttrNameIn', name).then(res => res.data);
};
export const makeBackfill = async (data) => {
	return await axios.post('type/backfill', data).then(res => res.data);
};