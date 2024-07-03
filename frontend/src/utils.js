
import { createListResource } from 'frappe-ui';

export const fetchDocTypes = async (doc, sidebarStore) => {
  const docTypesResource = createListResource({
    doctype: doc,
    fields: ['name', 'status'], // Ensure status is fetched
    orderBy: 'creation desc',
    start: 0,
    pageLength: 100,
  });

  try {
    await docTypesResource.list.fetch();
    if (docTypesResource.data && docTypesResource.data.length > 0) {
      const docTypes = docTypesResource.data.map((truck) => ({
        name: truck.name,
        status: truck.status, // Include status
      }));
      sidebarStore.setDocTypes(docTypes);
    } else {
      console.error("Failed to fetch data or no data available");
    }
  } catch (error) {
    console.error("Error fetching doc types:", error);
  } finally {
    return docTypesResource.data || [];
  }
};
