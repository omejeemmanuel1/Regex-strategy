import React, { useState } from 'react';
import './App.css';
import { ExtractedItem, ParseResponse } from './types';

const App: React.FC = () => {
  const [invoiceText, setInvoiceText] = useState<string>('');
  const [parsedData, setParsedData] = useState<ExtractedItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [editMode, setEditMode] = useState<boolean>(false);
  const [editableData, setEditableData] = useState<ExtractedItem[] | null>(null); 

  React.useEffect(() => {
    if (parsedData) {
      setEditableData(parsedData);
    }
  }, [parsedData]);

  const handleParse = async (): Promise<void> => {
    setLoading(true);
    setError(null);
    setParsedData(null);
    setEditMode(false); 
    setEditableData(null);

    try {
      const response = await fetch('http://localhost:8000/parse', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: invoiceText }),
      });

      if (!response.ok) {
        const errorData: { detail: string } = await response.json();
        throw new Error(errorData.detail || 'Something went wrong');
      }

      const data: ParseResponse = await response.json();
      setParsedData(data.extracted_items || []);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleEditChange = (
    e: React.ChangeEvent<HTMLInputElement>,
    index: number,
    field: keyof ExtractedItem
  ): void => {
    if (editableData) {
      const updatedData = [...editableData];
      updatedData[index] = { ...updatedData[index], [field]: e.target.value };
      setEditableData(updatedData);
    }
  };

  const handleSaveEdits = (): void => {
    if (editableData) {
      setParsedData(editableData);
      setEditMode(false); 
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Invoice Parser</h1>
      </header>
      <main>
        <textarea
          placeholder="Paste invoice text here..."
          value={invoiceText}
          onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setInvoiceText(e.target.value)}
          rows={10}
          cols={50}
        ></textarea>
        <br />
        <button onClick={handleParse} disabled={loading}>
          {loading ? 'Parsing...' : 'Parse Invoice'}
        </button>

        {loading && <p className="loading-message">Loading...</p>}
        {error && <p className="error-message">Error: {error}</p>}

        {parsedData && parsedData.length > 0 && (
          <div className="results-container">
            <h2>Extracted Items:</h2>
            <div className="edit-buttons">
              {!editMode ? (
                <button onClick={() => setEditMode(true)}>Edit</button>
              ) : (
                <button onClick={handleSaveEdits}>Save</button>
              )}
            </div>
            {(editMode ? editableData : parsedData)?.map((item, index) => (
              <div key={index} className="extracted-item">
                <p>
                  <strong>Product Name:</strong>{' '}
                  {editMode ? (
                    <input
                      type="text"
                      value={item.product_name || ''}
                      onChange={(e) => handleEditChange(e, index, 'product_name')}
                    />
                  ) : (
                    item.product_name || 'N/A'
                  )}
                </p>
                <p>
                  <strong>Quantity:</strong>{' '}
                  {editMode ? (
                    <input
                      type="number"
                      value={item.quantity || ''}
                      onChange={(e) => handleEditChange(e, index, 'quantity')}
                    />
                  ) : (
                    item.quantity || 'N/A'
                  )}
                </p>
                <p>
                  <strong>Unit:</strong>{' '}
                  {editMode ? (
                    <input
                      type="text"
                      value={item.unit || ''}
                      onChange={(e) => handleEditChange(e, index, 'unit')}
                    />
                  ) : (
                    item.unit || 'N/A'
                  )}
                </p>
                <p>
                  <strong>Price:</strong>{' '}
                  {editMode ? (
                    <input
                      type="number"
                      value={item.price || ''}
                      onChange={(e) => handleEditChange(e, index, 'price')}
                    />
                  ) : (
                    item.price || 'N/A'
                  )}
                </p>
                <p>
                  <strong>Unit Price:</strong>{' '}
                  {editMode ? (
                    <input
                      type="number"
                      value={item.unit_price || ''}
                      onChange={(e) => handleEditChange(e, index, 'unit_price')}
                    />
                  ) : (
                    item.unit_price || 'N/A'
                  )}
                </p>
              </div>
            ))}
          </div>
        )}
        {parsedData && parsedData.length === 0 && !loading && (
          <p>No items extracted.</p>
        )}
      </main>
    </div>
  );
}

export default App;
